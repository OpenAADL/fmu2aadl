Moonlanding AADL + FMI
======================

About
-----

This example is adapted from the Moonlanding example from Peter
Fritzon, as detailed in the `tutorial <https://openmodelica.org/images/docs/userdocs/modprod2012-tutorial1-Peter-Fritzson-ModelicaTutorial.pdf/>`_.

We adapted this example so that:

* the environment is modeled as a `Modelica` model, and turned into a
  FMU using the JModelica toolset
* the controller is implemented as a `C` function,
* the controller is integrated to the environment in an `AADL` model

From an code generation perpective:

* The ``fmu2aadl`` script generates the corresponding AADL for the
  environment elements, and the C wrapper function.
* ``ocarina`` is used to assemble all elements together.

Instructions
------------

* To compile this example: ``make build``
* To run this example: ``make run``

The program will run for 110 seconds, and ouput after each iteration
the result from the FMU computations in the file ``result.csv``.

See companion makefile for details

Notes
-----

The generated FMU targets GNU/Linux 64 bits, generated binary expect
the FMUs to be located in the current directory.

To regenerate the FMUs, go in ``Modelica`` directory and run the
``MoonLanding.py`` script.
