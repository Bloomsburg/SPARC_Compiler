## Sean Bloomsburg
## sbloomsburg@gmail.com
##
## This module gets the variable type
## of a variable defined in the source code.
##

import re


def get_type(variable, variable_symbol_table, procedure_symbol_table, inside_procedure):
    intermediate_re = re.compile('[A-Z]\$\d+')

    if type(variable) == str:
        if intermediate_re.search(variable):
            variable_type = variable
        else:
            if inside_procedure == False:
                key = variable
                found = False
                while found == False:
                    current_variable = variable_symbol_table[key]
                    if type(current_variable) == list:
                        for i in range(len(current_variable)):
                            element = current_variable[i]
                            if type(element) == tuple:
                                if element[0] == 'Type':
                                    variable_type = element[1]
                                    found = True
                                if element[0] == 'Attribute':
                                    key = element[1]    

            else:
                key = variable
                found = False
                while found == False:
                    current_variable = procedure_symbol_table[key]           
                    if type(current_variable) == list:
                        for i in range(len(current_variable)):
                            element = current_variable[i]
                            if type(element) == tuple:
                                if element[0] == 'Type':
                                    variable_type = element[1]
                                    found = True
                                if element[0] == 'Attribute':
                                    key = element[1]

    else:
        if inside_procedure == False:
            key = variable
            found = False
            while found == False:
                current_variable = variable_symbol_table[key]
                if type(current_variable) == list:
                    for i in range(len(current_variable)):
                        element = current_variable[i]
                        if type(element) == tuple:
                            if element[0] == 'Type':
                                variable_type = element[1]
                                found = True
                            if element[0] == 'Attribute':
                                key = element[1]

        else:
            key = variable
            found = False
            while found == False:
                current_variable = procedure_symbol_table[key]           
                if type(current_variable) == list:
                    for i in range(len(current_variable)):
                        element = current_variable[i]
                        if type(element) == tuple:
                            if element[0] == 'Type':
                                variable_type = element[1]
                                found = True
                            if element[0] == 'Attribute':
                                key = element[1]

    return variable_type

if __name__ == get_type:
    get_type()
