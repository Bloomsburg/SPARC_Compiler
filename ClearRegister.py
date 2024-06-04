## Sean Bloomsburg
## sbloomsburg@gmail.com
##
## This module handles clearing the registers
## for generating the assembly code. 
##


def clear_current_register(register_dictionary, reverse_register_dictionary, clear):
    key_list = register_dictionary.keys()
    registers = []

    ## Find all registers holding values
    for i in range(len(key_list)):
        key = key_list[i]
        if register_dictionary[key] != "EMPTY":
            registers.append(key)
            register_dictionary[key] = "EMPTY"

    reverse_register_dictionary = {}
    return registers, register_dictionary, reverse_register_dictionary, clear

if __name__ == clear_current_register:
    clear_current_register
