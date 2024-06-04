## Sean Bloomsburg
## sbloomsburg@gmail.com
##
## This module handles procedure declarations
## made by the source code for the CodeGenerator
## module.
##

import RegisterAllocation
import copy

def generate(tuple, global_lines, register_dictionary, reverse_register_dictionary, clear, incoming_variable):
    result = tuple[0]
    operation = tuple[1]
    operand1 = tuple[2]
    operand2 = tuple[3]
    comment =  "\t\t ! (" + str(result) + ", " + str(operation) + ", " + str(operand1) + ", " + str(operand2) + ")"

    if operation == 'FORMALVALUEPARAMETERS':
        reverse_register_dictionary[operand1] = "%i"+str(incoming_variable)
        incoming_variable = incoming_variable + 1

    if operation == 'FORMALREFERENCEPARAMETERS':
        incoming = "%i"+str(incoming_variable)
        incoming_variable = incoming_variable + 1
        load_register = "load_register"
        values = []
        values.append(load_register)
        register_allocation_output = RegisterAllocation.allocate(values, register_dictionary, reverse_register_dictionary, clear)
        values = register_allocation_output[0]
        register_dictionary = copy.copy(register_allocation_output[1])
        reverse_register_dictionary = copy.copy(register_allocation_output[2])
        clear = register_allocation_output[3]
        load_register = values[0]
        line = "\tld [" + incoming + "], " + str(load_register)
        global_lines.append('{0:20}{1:5}'.format(line, comment))

    if operation == 'REFERENCEPARAMETERS':
        if operand1 in reverse_register_dictionary:
            operand1 = reverse_register_dictionary[operand1]
        incoming = "%o"+str(incoming_variable)
        line = "\tmov " + operand1 + ", " + incoming

    if operation == 'IADD':
        if operand1 in reverse_register_dictionary:
            operand1 = reverse_register_dictionary[operand1]
        if operand2 in reverse_register_dictionary:
            operand2 = reverse_register_dictionary[operand2]

        line = "\tadd " +   str(operand1) + ", " + str(operand2) + ", %i0"
        global_lines.append('{0:20}{1:5}'.format(line, comment))

    if operation == 'ISUB':
        if operand1 in reverse_register_dictionary:
            operand1 = reverse_register_dictionary[operand1]
        if operand2 in reverse_register_dictionary:
            operand2 = reverse_register_dictionary[operand2]

        line = "\tsub " +   str(operand1) + ", " + str(operand2) + ", %i0"
        global_lines.append('{0:20}{1:5}'.format(line, comment))

    return global_lines, register_dictionary, reverse_register_dictionary, clear, incoming_variable

if __name__ == generate:
    generate
