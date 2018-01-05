FMU2AADL
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

Add $HOME/.local/bin to your PATH

Authors
-------

Jean-Marie Gauthier, Samares Engineering
Jerome Hugues, ISAE Supaero
