#!/usr/bin/env python

from lxml import etree

import zipfile
import shutil, sys, os
from distutils.dir_util import copy_tree

################################################################################
def _unzipModelDescriptionFile(path):
    '''Unzip FMU and extract the model description XML file

    :param path: full path to FMU file
    :type path: string
    '''

    zip_ref = zipfile.ZipFile(path, 'r')
    zip_ref.extract("modelDescription.xml", "", "")
    zip_ref.close()

################################################################################
def FMU2AADL_Prologue(root, file):
    '''Build the prologue of an AADL package

    :param root: root of the FMU XML tree
    :param file: file to output

    '''

    file.write('-- This file has been automatically generated. DO NOT EDIT\n')
    file.write('\n')
    file.write('package ' + root.get('modelName') + '_FMU\n')
    file.write('public\n')
    file.write(3 * ' ' + 'with FMI;\n')
    file.write('\n')

################################################################################
def FMU2AADL_Epilogue(root, file):
    '''Build the epilogue of an AADL package

    :param root: root of the FMU XML tree
    :param file: file to output

    '''
    file.write('end ' + root.get('modelName') + '_FMU;\n')
    file.close()

################################################################################
def FMU2AADL_MapScalarVariable(tree, file,thread_port):

    # The following dictionnaries define XML to AADL text mappings

    causality_map = { 'input' : ': in ',
                      'output' : ': out ' }

    variability_map = { 'continuous' : 'data port ',
                        'discrete' : 'even port ' }

    type_map = { 'real' : 'FMI::fmi2Real',
                 'integer' : 'FMI::fmi2Integer',
                 'boolean' : 'FMI::fmi2Boolean' }

    fmu_type=''

    # Iterate over the set of ScalarVariable nodes
    # Note: we map only inputs and outpus, parameters are discarded from now

    for svar in tree.xpath("/fmiModelDescription/ModelVariables/ScalarVariable"):
        if svar.get('causality') == 'input' or \
           svar.get('causality') == 'output':

            # Get the actual type, it is one child node of the current node

            for elt in svar:
                tag = elt.tag.lower()
                if tag in {'real', 'boolean','integer'}:
                    fmu_type = tag

            # Map the node to an AADL feature

            file.write(6 * ' ' + Map_Name(svar))               # port name
            file.write(causality_map[svar.get('causality')])     # direction
            if (thread_port):                                    # category
                if (svar.get('variability')):
                    file.write(variability_map[svar.get('variability')])
                else:
                    file.write(variability_map['continuous'])
            else:
                file.write("parameter ")

            file.write(type_map[fmu_type])                       # port type
            file.write ('; \n')

################################################################################
def FMU2AADL_Thread(root,tree,file,period):
    file.write(3 * ' ' + 'thread ' + root.get('modelName') + '_thread \n')
    file.write(3 * ' ' + 'features \n')

    FMU2AADL_MapScalarVariable(tree, file, True)

    file.write(3 * ' ' + 'properties\n')
    file.write(6 * ' ' + 'Dispatch_Protocol => Periodic;\n')
    file.write(6 * ' ' + 'Period => '+ period + 'ms;\n')
    file.write(6 * ' ' + 'Initialize_Entrypoint_Source_Text => "'
               + root.get('modelName').lower()
               + '_fmu_activate_entrypoint";\n')
    file.write(3 * ' ' + 'end ' + root.get('modelName') + '_thread;\n')
    file.write('\n')

################################################################################
def Map_Name(svar):
    map_name = "FMI_" + svar.get('name').replace("@","_") # Remove '@'
    map_name = map_name[:-1] if map_name.endswith('_') else map_name

    return map_name

################################################################################
def FMU2AADL_Thread_Impl(root,tree,file):
    file.write(3 * ' ' + 'thread implementation ' + root.get('modelName')
               + '_thread.impl \n')
    file.write(3 * ' ' + 'calls C: { \n')
    file.write(6 * ' ' + 'P_Spg : subprogram '
               + root.get('modelName') + '_spg;\n')
    file.write(3 * ' ' + '};\n')

    file.write(3 * ' ' + 'connections\n')

    cnx_index = 0
    for svar in tree.xpath("/fmiModelDescription/ModelVariables/ScalarVariable"):
        if svar.get('causality') == 'input':
            file.write(6 * ' ' + 'C' + str(int(cnx_index)) +': port '
                       + Map_Name(svar) + '-> P_Spg.'
                       + Map_Name(svar) + ';\n')
            cnx_index = cnx_index + 1

        if svar.get('causality') == 'output':
            file.write(6 * ' ' + 'C' + str(cnx_index) + ': port P_Spg.'
                       + Map_Name(svar) + '-> ' + Map_Name(svar)
                       + ';\n')
            cnx_index = cnx_index + 1

    file.write('\n')
    file.write(3 * ' ' + 'end ' + root.get('modelName') + '_thread.impl;\n')
    file.write('\n')

################################################################################
def FMU2AADL_Subprogram(root,tree,file):
    file.write(3 * ' ' + 'subprogram ' + root.get('modelName') + '_spg \n')
    file.write(3 * ' ' + 'features \n')

    FMU2AADL_MapScalarVariable(tree, file, False)

    file.write(3 * ' ' + 'properties\n')
    file.write(6 * ' ' + 'Source_Language => (C);\n')
    file.write(6 * ' ' + 'Source_Name => "' + root.get('modelName').lower()
               + '_fmu_entrypoint";\n')
    file.write(6 * ' ' + 'Source_Text => ("' + root.get('modelName').lower()
               + '_fmu_wrapper.c");\n')
    file.write(3 * ' ' + 'end ' + root.get('modelName') + '_spg;\n')
    file.write('\n')

################################################################################
def FMU2C_Wrapper(root,tree,file, fmu_file, period, duration):

    ctxName = root.get('modelName').lower() + '_ctx'
    fmu_file_full_path = os.path.abspath(fmu_file)

    file.write ('#include <stdbool.h>\n')
    file.write ('#include <stdio.h>\n')
    file.write ('#include <stdlib.h>\n')
    file.write ('#include "fmi2.h"\n')
    file.write ('#include "sim_support.h"\n')
    file.write ('#include "fmu_wrapper.h"\n')
    file.write ('\n')

    file.write('FMUContext ' + ctxName + ';\n')
    file.write('\n');

    # Activation entrypoint

    file.write('void ' + root.get('modelName').lower()
               + '_fmu_activate_entrypoint (void) {\n')
    file.write(2 * ' ' + 'const char     *fmuFileName ="' + fmu_file_full_path + '";\n')
    file.write(2 * ' ' + 'double          tEnd = ' + duration + ';\n')
    file.write(2 * ' ' + 'double          h = ' + period + ' / 1000.0;\n')
    file.write('\n');

    file.write(2 * ' ' + ctxName + '.fmu = malloc (sizeof (FMU));\n');
    file.write(2 * ' '
               + 'FMU_Activate_Entrypoint (fmuFileName, tEnd, h, &'
               + ctxName + ');\n');
    file.write('}\n');
    file.write('\n');

    # Compute entrypoint function

    is_first_arg = True
    file.write('void ' + root.get('modelName').lower() + '_fmu_entrypoint \n')

    for svar in tree.xpath("/fmiModelDescription/ModelVariables/ScalarVariable"):
        if svar.get('causality') == 'input':
            if is_first_arg:
                file.write(6 * ' ' + '(')
                is_first_arg = False
            else:
                file.write (',\n')
                file.write(7 * ' ')

            file.write ('fmi2Real ' + Map_Name(svar))

        if svar.get('causality') == 'output':
            if is_first_arg:
                file.write(6 * ' ' + '(')
                is_first_arg = False
            else:
                file.write (',\n')
                file.write(7 * ' ')

            file.write('fmi2Real *' + Map_Name(svar))

    file.write (') \n{\n');
    file.write(2 * ' ' + 'double          tEnd = ' + duration + ';\n')
    file.write(2 * ' ' + 'FMUContext ctx = ' + root.get('modelName').lower() + '_ctx;\n\n')
    file.write(2 * ' ' + '/* Main compute entrypoint */\n');
    file.write(2 * ' ' + 'fmi2ValueReference vr;\n');
    file.write(2 * ' ' + 'fmi2Real        r;\n');
    file.write(2 * ' ' + 'fmi2Status      fmi2Flag;\n\n');

    file.write(2 * ' ' + '/* Get the scalar variables */\n');
    for svar in tree.xpath("/fmiModelDescription/ModelVariables/ScalarVariable"):
        if svar.get('causality') == 'input' or svar.get('causality') == 'output':
            file.write(2 * ' ' + 'ScalarVariable *' + Map_Name(svar) + '_sv'
                       + ' = getVariable (' + ctxName + '.fmu->modelDescription, "'
                       + svar.get('name') + '");\n')
    file.write('\n');

    file.write (2 * ' ' + '/* Set the input */\n')
    for svar in tree.xpath("/fmiModelDescription/ModelVariables/ScalarVariable"):
        if svar.get('causality') == 'input':
            file.write(2 * ' ' + 'vr = getValueReference (' + Map_Name(svar)
                       + '_sv);\n')
            file.write (2 * ' '
                        + 'fmi2Flag = ' + ctxName + '.fmu->setReal (ctx.component, &vr, 1, &'
                        + Map_Name(svar) + ');\n')
    file.write('\n')

    file.write (2 * ' ' +  '/* Calculate the Step */\n')
    file.write (2 * ' ' +  'doStep (' + ctxName + '.fmu, ' + ctxName + '.component,\n')
    file.write (10 * ' ' +  '' + ctxName + '.currentCommunicationPoint,\n')
    file.write (10 * ' ' +  '' + ctxName + '.communicationStepSize,\n')
    file.write (10 * ' ' +  '' + ctxName + '.noSetFMUStatePriorToCurrentPoint);\n')
    file.write('\n');
    file.write (2 * ' ' +  '/* Dump values */\n')
    file.write (2 * ' ' +  'outputRow (ctx.fmu, ctx.component,\n')
    file.write (13 * ' ' +  'ctx.currentCommunicationPoint,\n')
    file.write (13 * ' ' +  "ctx.resultFile, ',', fmi2False);\n")
    file.write('\n');

    file.write (2 * ' ' +  '/* Get the outputs */\n')
    for svar in tree.xpath("/fmiModelDescription/ModelVariables/ScalarVariable"):
        if svar.get('causality') == 'output':
            file.write(2 * ' ' + 'vr = getValueReference (' + Map_Name(svar)
                       + '_sv);\n')
            file.write(2 * ' '
                       + 'fmi2Flag = ' + ctxName + '.fmu->getReal (' + ctxName + '.component, &vr, 1, &r);\n')
            file.write (2 * ' ' + '*' + Map_Name(svar) + '= r;\n')
            file.write('\n');

    file.write(2 * ' '
               + '' + ctxName + '.currentCommunicationPoint += ' + ctxName + '.communicationStepSize;\n');
    file.write('\n');
    file.write(2 * ' ' + '/* 3) terminate the simulation */\n');
    file.write('\n');
    file.write(2 * ' ' + 'if (' + ctxName + '.currentCommunicationPoint > tEnd)  {\n');
    file.write(4 * ' ' + 'freeContext (' + ctxName + ');\n');
    file.write(4 * ' ' + 'exit (0);\n');
    file.write(2 * ' ' + '}\n');
    file.write('}\n');

    file.close()

################################################################################
def fmu2aadl(fmu_file, period, duration):
    '''
    Map a FMU to an AADL package

    :param fmu_file: full path to FMU file
    :type fmu_file: string

    '''

    # Unzip FMU

    _unzipModelDescriptionFile(fmu_file)

    # Parse XML FMU description

    tree = etree.parse("modelDescription.xml")
    root = tree.getroot()

    # Build output AADL file, name is deduced from FMU name

    aadlFile = root.get('modelName').lower() + '_fmu.aadl'
    file = open(aadlFile,'w')
    print "Generating AADL file: " + aadlFile

    FMU2AADL_Prologue(root, file)
    FMU2AADL_Subprogram(root,tree,file)
    FMU2AADL_Thread(root,tree,file,period)
    FMU2AADL_Thread_Impl(root,tree,file)
    FMU2AADL_Epilogue(root, file)

    # Build C wrapper file

    cFile = root.get('modelName').lower() + '_fmu_wrapper.c'
    file = open(cFile,'w')
    print "Generating C file: " + cFile

    FMU2C_Wrapper (root, tree, file, fmu_file, period, duration)

    # Copy required runtime files

    shutil.copy(os.path.dirname(__file__) + "/fmu_wrapper.c", ".")
    shutil.copy(os.path.dirname(__file__) + "/fmu_wrapper.h", ".")
    shutil.copy(os.path.dirname(__file__) + "/userdefined.mk", ".")
    print "Copied fmu_wrapper.(c|h) and userdefined.mk to current directory"

    copy_tree(os.path.dirname(__file__) + "/fmusdk2.0.3", "./fmusdk2.0.3")

    # Clean-up

    os.remove("modelDescription.xml")
