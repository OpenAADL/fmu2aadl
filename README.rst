FMU2AADL  |license|
========

About
-----

The `fmu2aadl` script maps FMU to AADL package that can be later
integrated into larger AADL models, to simulate larger systems, and
additional makefiles and C compilation units for integration with
Ocarina.

This package embeds a copy of the FMUSDK2.0.3 ported to Linux by
Christopher Brooks from https://github.com/cxbrooks/fmusdk2

Installation
------------

The script is provided as a standard Python module.

The script can be installed, as user, using default Python install
procedure::

  python setup.py install --user

Do not forget to add ``$HOME/.local/bin`` to your PATH.

Dependencies: The script assumes ``libxml2`` is installed, along with a fully 
operational ``Ocarina``, and a gcc + binutils compilation chain.

Authors
-------

* Jean-Marie Gauthier, Samares Engineering
* Jerome Hugues, ISAE Supaero

.. |license| image:: https://img.shields.io/badge/License-EPL%201.0-red.svg
    :target: https://github.com/OpenAADL/fmu2aadl/
    :alt: License
