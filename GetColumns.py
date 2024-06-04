## Sean Bloomsburg
## sbloomsburg@gmail.com
##
## This module finds the finds the number
## of columns in a matrix defined in the source. 
##


def get_columns(variable, variable_symbol_table, procedure_symbol_table, procedure):

    if procedure == False:
        key = variable
        found = False
        while found == False:
            current_variable = variable_symbol_table[key]
            if type(current_variable) == list:
                for i in range(len(current_variable)):
                    element = current_variable[i]
                    if type(element) == tuple:
                        if element[0] == "Columns":
                            columns = element[1]
                            found = True

    else:
        key = variable
        found = False
        while found == False:
            current_variable = procedure_symbol_table[key]           
            if type(current_variable) == list:
                for i in range(len(current_variable)):
                    element = current_variable[i]
                    if type(element) == tuple:
                        if element[0] == "Columns":
                            columns = element[1]
                            found = True

    return columns

if __name__ == get_columns:
    get_columns()
