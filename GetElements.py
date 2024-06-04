## Sean Bloomsburg
## sbloomsburg@gmail.com
##
## This module gets the elements in an array.
##


def get_elements(variable, variable_symbol_table, procedure_symbol_table, procedure):

    if procedure == False:
        key = variable
        found = False
        while found == False:
            currentvariable = variable_symbol_table[key]
            if type(currentvariable) == list:
                for i in range(len(currentvariable)):
                    variable_element = currentvariable[i]
                    if type(variable_element) == tuple:
                        if variable_element[0] == 'Elements':
                            elements = variable_element[1]
                            found = True

    else:
        key = variable
        found = False
        while found == False:
            currentvariable = procedure_symbol_table[key]           
            if type(currentvariable) == list:
                for i in range(len(currentvariable)):
                    variable_element = currentvariable[i]
                    if type(variable_element) == tuple:
                        if variable_element[0] == 'Elements':
                            elements = variable_element[1]
                            found = True

    return elements

if __name__ == get_elements:
    get_elements()
