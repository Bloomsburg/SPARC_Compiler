## Sean Bloomsburg
## sbloomsburg@gmail.com
##
## This module handles register allocation
## for generating the assembly code. 
##


def allocate(values, register_dictionary, reverse_register_dictionary, clear):
    key_list = register_dictionary.keys()

    for value in values:

        ## Search for empty register
        for key in key_list:
            if register_dictionary[key] == "EMPTY":
                reverse_register_dictionary[value] = key
                register_dictionary[key] = value
                return values, register_dictionary, reverse_register_dictionary, clear

        ## Clear registers of intermediate results
        for key in key_list:
            if str(register_dictionary[key])[0:2] == "I$":
                register_dictionary[key] = "EMPTY"
                clear = True              

        ## Search for empty register
        for key in key_list:
            if register_dictionary[key] == "EMPTY":
                reverse_register_dictionary[value] = key
                register_dictionary[key] = value
                return values, register_dictionary, reverse_register_dictionary, clear

        ## Search for register with constant        
        for key in key_list:
            if type(register_dictionary[key]) == int:
                register_dictionary[key] = value
                reverse_register_dictionary[value] = key
                clear = True
                return values, register_dictionary, reverse_register_dictionary, clear

        ## Search for register with variable
        for key in key_list:
            if type(register_dictionary[key]) == str:
                reverse_register_dictionary[value] = key
                register_dictionary[key] = value
                clear = True
                return values, register_dictionary, reverse_register_dictionary, clear

    return values, register_dictionary, reverse_register_dictionary, clear

if __name__ == allocate:
    allocate
