###############################################################################
# Ocarina/FMI docker image, based on a debian image
#
# This docker file fetches all dependencies to compile Ocarina, along
# with the build_ocarina.sh build script
#
# To build the image:
#    docker build -t ocarina/fmi .
#
# To run the image:
#    docker run -t -i ocarina/fmi bash
#
###############################################################################

###############################################################################
# Baseline: debian 10 (buster)
#

FROM debian:buster
MAINTAINER Jerome Hugues <hugues.jerome@gmail.com>

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
            git wget ca-certificates \
            autoconf automake gnat gprbuild build-essential \
            python python-dev python-setuptools python-lxml python-docopt \
            sudo procps \
            libxml2-dev unzip libgfortran5

# Note on installed packages
# * git + wget + ca-certificates             : fetch source from repositories
# * autoconf automake gnat gprbuild build-essential : compilation chain
# * python python-dev python-setuptools      : testsuite + FMI manipulation
#   python-lxml
# * libxml2-dev unzip libgfortran5           : for FMI .fmu manipulation

###############################################################################
# Install default "ocarina" user
# Add Ocarina user to sudoers for building .deb

RUN useradd -m -c "ocarina" -s /bin/bash ocarina && echo "ocarina:ocarina" | chpasswd
RUN adduser ocarina sudo

VOLUME /work

# Set up account and fetch fresh copy of ocarina-build repository

USER ocarina
ENV PATH /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/home/ocarina/.local/bin:/home/ocarina/local/bin
ENV TERM xterm
ENV LANG en_US
ENV LC_ALL en_US.UTF-8
WORKDIR /home/ocarina

# Install Ocarina

RUN cd $HOME && git clone https://github.com/OpenAADL/ocarina-build.git && \
    cd $HOME/ocarina-build && \
    ./build_ocarina.sh --self-update && \
    ./build_ocarina.sh --scenario=fresh-install --prefix=$HOME/local

# Install fmu2aadl

RUN cd $HOME && git clone https://github.com/OpenAADL/fmu2aadl.git && \
    cd fmu2aadl && python setup.py install --user

CMD bash