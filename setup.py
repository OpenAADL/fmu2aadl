from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name             = 'fmu2aadl',
      version          = '0.1',
      url = 'https://github.com/OpenAADL/fmu2aadl',
      description      = 'FMU-to-AADL converter',
      long_description = readme(),
      classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: Eclipse Public License 1.0 (EPL-1.0)',
          'Programming Language :: Python :: 2.7',
          'Topic :: Software Development :: Code Generators',
      ],
      license = "EPL-1.0",
      packages         = ['fmu2aadl'],
      entry_points     = {
          'console_scripts' : ['fmu2aadl=fmu2aadl.command_line:main'],
      },
      install_requires=[
          'docopt', 'lxml',
      ],
      include_package_data = True,
      zip_safe = False
)
