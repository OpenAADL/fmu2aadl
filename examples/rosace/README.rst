ROSACE AADL + FMI
==================

About
-----
 
This package models the case study from "Pagetti, Claire and Saussie, David and Gratia, Romain and Noulard, Eric and Siron, Pierre "The ROSACE Case Study: From Simulink Specification to Multi/Many-Core Execution." (2014) In: Journees FAC - Formalisation des Activités Concurrentes, 16 April 2014 - 17 April 2014 (Toulouse, France).

We adapted this example so that:

* the Aircraft_Dynamic, Elevator and Engine components are modeled as a `Modelica` model in ``Modelica`` directory, and turned into a FMU using the JModelica toolset. A variant of these components are also proposed directly in C for reference comparison,
* all other components are implemented in C,
* the controller is integrated to the environment in an `AADL` model

From a code generation perpective:

* The ``fmu2aadl`` script generates the corresponding AADL for the
  environment elements, and the C wrapper function.
* ``ocarina`` is used to assemble all elements together.

Two variants are proposed for comparison

* a pure C implementation
* a mix of C and FMUs blocks

Instructions
------------

* To compile this example: ``make build``
* To run this example: ``make run``

The program will run for 110 seconds, and ouput after each iteration the result from the
FMU computations in the file ``result.csv``.

See companion makefile for details

Notes
-----

The generated FMU targets GNU/Linux 64 bits, generated binary expect
the FMUs to be located in the current directory.

