## Sean Bloomsburg
## sbloomsburg@gmail.com
##
## This module determines the semantic meaning
## of the syntactical units in the tokens and
## builds the Symbol Table.
##

import copy
import GetType
import GetColumns
import GetElements
import re
import string


def analyze(semantic_stack, variable_symbol_table, procedure_symbol_table, production_number, handle_length, inside_procedure, flags_dictionary, intermediate_code, declared_variable_list, local_declared_variable_list, label_list):
    if flags_dictionary["12"]:
         print "\nThis is the semantic stack before reduction: ", semantic_stack

    ##Handles production 1: start --> prog body END
    if production_number == 0:
        ##Retrieve name at s_i2
        variable = semantic_stack[len(semantic_stack) - 3]

        ##4-tuple
        result = variable
        operation = "ENDPROGRAM"
        operand1 = "-"
        operand2 = "-"
        tuple = (result, operation, operand1, operand2)
        intermediate_code.append(tuple)

        if flags_dictionary["13"]:
            print "\nThis is the intermediate 4-tuple produced by production 1: ", tuple

    ##Handles production 2: prog --> PROGRAM variable
    if production_number == 1:

        ##Insert string at s_i into into symbol table
        variable = semantic_stack[len(semantic_stack) - 1]
        
        if variable in declared_variable_list:
            print "\nThere has been a variable declaration error!"
            print "The variable ", variable, " has been double declared."
            print "It will maintain its first declared value."

        else:
            variable_symbol_table[variable] = [("Type", "PROGRAM")]
            semantic_stack[len(semantic_stack) - 2] = variable

        if flags_dictionary["15"]:
            print "\nThis is the variable symbol table entry just made: ", variable, variable_symbol_table[variable]

        ##4-tuple
        result = "-"
        operation = "PROGRAMBEGIN"
        operand1 = variable
        operand2 = "-"
        tuple = (result, operation, operand1, operand2)
        intermediate_code.append(tuple)

        if flags_dictionary["13"]:
            print "\nThis is the intermediate 4-tuple produced by production 2: ", tuple

    ##Handles production 5: declpart --> DECLARE decllist END
    if production_number == 4:
        variable = semantic_stack[len(semantic_stack) - 2]
        
        ##4-tuple
        result = "-"
        operation = "ENDDECLARATIONS"
        operand1 = "-"
        operand2 = "-"
        tuple = (result, operation, operand1, operand2)
        intermediate_code.append(tuple)
        semantic_stack[len(semantic_stack) - 3] = variable

        if flags_dictionary["13"]:
            print "\nThis is the intermediate 4-tuple produced by production 5: ", tuple

    ##Handles production 8: declstat --> declstat , variable
    if production_number == 7:

        ##Insert string at s_i into into symbol table
        if inside_procedure == False:
            variable = semantic_stack[len(semantic_stack) - 1]
            attribute = semantic_stack[len(semantic_stack) - 3]
            
            if variable in declared_variable_list:
                print "\nThere has been a variable declaration error!"
                print "The variable ", variable, " has been doubly declared."
                print "It will maintain its first declared value."

            else:
                attributes = variable_symbol_table[attribute]
                variable_symbol_table[variable] = attributes
                semantic_stack[len(semantic_stack) - 3] = variable

            if flags_dictionary["15"]:
                print "\nThis is the variable symbol table entry just made: ",variable, variable_symbol_table[variable]

        ##Insert string at s_i into local symbol table if inside procedure
        if inside_procedure == True:
            variable = semantic_stack[len(semantic_stack) - 1]
            attribute = semantic_stack[len(semantic_stack) - 3]

            if variable in local_declared_variable_list:
                print "\nThere has been a variable declaration error!"
                print "The variable ", variable, " has been doubly declared."
                print "It will maintain its first declared value."

            else:
                attributes = procedure_symbol_table[attribute]
                procedure_symbol_table[variable] = attributes
                semantic_stack[len(semantic_stack) - 3] = variable 

            if flags_dictionary["15"]:
                print "\nThis is the variable symbol table entry just made: ", variable, procedure_symbol_table[variable]

        ##4-tuple
        result = variable
        operation = "MEMORY"
        operand1 = "-"
        operand2 = "-"
        tuple = (result, operation, operand1, operand2)
        intermediate_code.append(tuple)

        if flags_dictionary["13"]:
            print "\nThis is the intermediate 4-tuple produced by production 8: ", tuple

    ##Handles production 9: declstat --> declstat , variable = integer
    if production_number == 8:

        ##Insert string at s_i2 into symbol table
        if inside_procedure == False:
            variable = semantic_stack[len(semantic_stack) - 3]
            attribute = semantic_stack[len(semantic_stack) - 5]
            s_i = semantic_stack[len(semantic_stack) - 1]
            
            if variable in declared_variable_list:
                print "\nThere has been a variable declaration error!"
                print "The variable ", variable, " has been doubly declared."
                print "It will maintain its first declared value."

            else:
                attributes = variable_symbol_table[attribute]
                variable_symbol_table[variable] = attributes
                semantic_stack[len(semantic_stack) - 5] = variable          

            if flags_dictionary["15"]:
                print "\nThis is the variable symbol table entry just made: ", variable, variable_symbol_table[variable]

        ##Insert string at s_i2 into local symbol table if inside procedure
        if inside_procedure == True:
            variable = semantic_stack[len(semantic_stack) - 3]
            attribute = semantic_stack[len(semantic_stack) - 5]
            s_i = semantic_stack[len(semantic_stack) - 1]
            
            if variable in local_declared_variable_list:
                print "\nThere has been a variable declaration error!"
                print "The variable ", variable, " has been doubly declared."
                print "It will maintain its first declared value."

            else:
                attributes = procedure_symbol_table[attribute]
                procedure_symbol_table[variable] = attributes
                semantic_stack[len(semantic_stack) - 5] = variable

            if flags_dictionary["15"]:
                print "\nThis is the variable symbol table entry just made: ", variable, procedure_symbol_table[variable]

        ##4-tuple
        result = variable
        operation = "INITIALIZEMEMORY"
        operand1 = s_i
        operand2 = "-"
        tuple = (result, operation, operand1, operand2)
        intermediate_code.append(tuple)

        if flags_dictionary["13"]:
            print "\nThis is the intermediate 4-tuple produced by production 9: ", tuple

    ##Handles production 10: declstat --> type variable
    if production_number == 9:
        
        ##Insert string at s_i into into symbol table
        if inside_procedure == False:
            variable = semantic_stack[len(semantic_stack) - 1]
            type = semantic_stack[len(semantic_stack) - 2]
            if variable in declared_variable_list:
                print "\nThere has been a variable declaration error!"
                print "The variable ", variable, " has been doubly declared."
                print "It will maintain its first declared value."
            else:
                variable_symbol_table[variable] = [("Type", type), ("Shape", "SCALAR"), ("Size", 1)]
                semantic_stack[len(semantic_stack) - 2] = variable
                
            if flags_dictionary["15"]:
                print "\nThis is the variable symbol table entry just made: ",variable, variable_symbol_table[variable]

        ##Insert string at s_i into local symbol table if inside procedure
        if inside_procedure == True:
            variable = semantic_stack[len(semantic_stack) - 1]
            type = semantic_stack[len(semantic_stack) - 2]
            if variable in local_declared_variable_list:
                print "\nThere has been a variable declaration error!"
                print "The variable ", variable, " has been doubly declared."
                print "It will maintain its first declared value."

            else:
                procedure_symbol_table[variable] = [("Type", type), ("Shape", "SCALAR"), ("Size", 1)]
                semantic_stack[len(semantic_stack) - 2] = variable

            if flags_dictionary["15"]:
                print "\nThis is the variable symbol table entry just made: ", variable, procedure_symbol_table[variable]            

        ##4-tuple
        result = variable
        operation = "INITIALIZEMEMORY"
        operand1 = 1
        operand2 = "-"
        tuple = (result, operation, operand1, operand2)
        intermediate_code.append(tuple)

        if flags_dictionary["13"]:
            print "\nThis is the intermediate 4-tuple produced by production 10: ", tuple

    ##Handles production 11: declstat --> type variable = integer
    if production_number == 10:

        ##Insert string at s_i2 into symbol table
        if inside_procedure == False:
            value = semantic_stack[len(semantic_stack) - 1]            
            variable = semantic_stack[len(semantic_stack) - 3]
            type = semantic_stack[len(semantic_stack) - 4]
            if variable in declared_variable_list:
                print "\nThere has been a variable declaration error!"
                print "The variable ", variable, " has been doubly declared."
                print "It will maintain its first declared value."

            else:
                variable_symbol_table[variable] = [("Type", type), ("Shape", "SCALAR"), ("Size", 1)]
                semantic_stack[len(semantic_stack) - 4] = variable

            if flags_dictionary["15"]:
                print "\nThis is the variable symbol table entry just made: ",variable, variable_symbol_table[variable]

        ##Insert string at s_i2 into local symbol table if inside procedure
        if inside_procedure == True:
            value = semantic_stack[len(semantic_stack) - 1]            
            variable = semantic_stack[len(semantic_stack) - 3]
            type = semantic_stack[len(semantic_stack) - 4]
            if variable in local_declared_variable_list:
                print "\nThere has been a variable declaration error!"
                print "The variable ", variable, " has been doubly declared."
                print "It will maintain its first declared value."

            else:
                procedure_symbol_table[variable] = [("Type", type), ("Shape", "SCALAR"), ("Size", 1)]
                semantic_stack[len(semantic_stack) - 4] = variable

            if flags_dictionary["15"]:
                print "\nThis is the variable symbol table entry just made: ", variable, procedure_symbol_table[variable]

        ##4-tuple
        result = variable
        operation = "INITIALIZEMEMORY"
        operand1 = value
        operand2 = "-"
        tuple = (result, operation, operand1, operand2)
        intermediate_code.append(tuple)

        if flags_dictionary["13"]:
            print "\nThis is the intermediate 4-tuple produced by production 11: ", tuple

    ##Handles production 12: declstat --> type variable integer
    if production_number == 11:

        ##Insert string at s_i1 into symbol table
        if inside_procedure == False:
            variable = semantic_stack[len(semantic_stack) - 2]
            type = semantic_stack[len(semantic_stack) - 3]
            s_i = semantic_stack[len(semantic_stack) - 1]
            if variable in declared_variable_list:
                print "\nThere has been a variable declaration error!"
                print "The variable ", variable, " has been doubly declared."
                print "It will maintain its first declared value."

            else:
                variable_symbol_table[variable] = [("Type", type), ("Shape", "VECTOR"), ("Elements", s_i)]
                semantic_stack[len(semantic_stack) - 3] = variable

            if flags_dictionary["15"]:
                print "\nThis is the variable symbol table entry just made: ",variable, variable_symbol_table[variable]

        ##Insert string at s_i1 into local symbol table if inside procedure
        if inside_procedure == True:
            variable = semantic_stack[len(semantic_stack) - 2] 
            type = semantic_stack[len(semantic_stack) - 3]
            s_i = semantic_stack[len(semantic_stack) - 1]
            if variable in local_declared_variable_list:
                print "\nThere has been a variable declaration error!"
                print "The variable ", variable, " has been doubly declared."
                print "It will maintain its first declared value."

            else:
                procedure_symbol_table[variable] = [("Type", type), ("Shape", "VECTOR"), ("Elements", s_i)]
                semantic_stack[len(semantic_stack) - 3] = variable
            
            if flags_dictionary["15"]:
                print "\nThis is the variable symbol table entry just made: ", variable, procedure_symbol_table[variable]
                
        ##4-tuple
        result = variable
        operation = "MEMORY"
        operand1 = s_i
        operand2 = "-"
        tuple = (result, operation, operand1, operand2)
        intermediate_code.append(tuple)

        if flags_dictionary["13"]:
            print "\nThis is the intermediate 4-tuple produced by production 12: ", tuple

    ##Handles production 13: declstat --> type variable integer :: integer
    if production_number == 12:

        ##Insert string at s_i3 into symbol table
        if inside_procedure == False:
            variable = semantic_stack[len(semantic_stack) - 4]
            type = semantic_stack[len(semantic_stack) - 5]
            columns = semantic_stack[len(semantic_stack) - 1]
            rows = semantic_stack[len(semantic_stack) - 3]

            if variable in declared_variable_list:
                print "\nThere has been a variable declaration error!"
                print "The variable ", variable, " has been doubly declared."
                print "It will maintain its first declared value."

            else:
                variable_symbol_table[variable] = [("Type", type), ("Shape", "MATRIX"), ("Rows", rows), ("Columns", columns)]
                semantic_stack[len(semantic_stack) - 5] = variable

            if flags_dictionary["15"]:
                print "\nThis is the variable symbol table entry just made: ",variable, variable_symbol_table[variable]

        ##Insert string at s_i3 into local symbol table if inside procedure
        if inside_procedure == True:
            variable = semantic_stack[len(semantic_stack) - 4]          
            type = semantic_stack[len(semantic_stack) - 5]
            columns = semantic_stack[len(semantic_stack) - 1]
            rows = semantic_stack[len(semantic_stack) - 3]  
            if variable in local_declared_variable_list:
                print "\nThere has been a variable declaration error!"
                print "The variable ", variable, " has been doubly declared."
                print "It will maintain its first declared value."

            else:
                procedure_symbol_table[variable] = [("Type", type), ("Shape", "MATRIX"), ("Rows", rows), ("Columns", columns)]  
                semantic_stack[len(semantic_stack) - 5] = variable

            if flags_dictionary["15"]:
                print "\nThis is the variable symbol table entry just made: ", variable, procedure_symbol_table[variable]

        ##4-tuple
        result = variable
        operation = "MEMORY"
        operand1 = rows
        operand2 = columns
        tuple = (result, operation, operand1, operand2)
        intermediate_code.append(tuple)

        if flags_dictionary["13"]:
            print "\nThis is the intermediate 4-tuple produced by production 13: ", tuple

    ##Handles production 14: type --> INTEGER
    if production_number == 13:

        ##Set s_i to "integer"
        s_i = len(semantic_stack) - 1
        semantic_stack[s_i] = "INTEGER"

    ##Handles production 15: type --> REAL
    if production_number == 14:

        ##Set s_i to "real"
        s_i = len(semantic_stack) - 1
        semantic_stack[s_i] = "REAL"

    ##Handles production 19: proc --> prochead declpart statlist END
    if production_number == 18:

        ##Retrieve name at s_i3
        s_i3 = semantic_stack[len(semantic_stack) - 4]

        if flags_dictionary["14"]:
            print "\nThis was the Local Variable Symbol Table inside a procedure: ", procedure_symbol_table

        ##Destroy local symbol table
        procedure_symbol_table = {}
        local_declared_variable_list = []
        procedure = False
        
        ##4-tuple
        result = s_i3
        operation = "ENDPROCEDURE"
        operand1 = "-"
        operand2 = "-"
        tuple = (result, operation, operand1, operand2)
        intermediate_code.append(tuple)
        
        if flags_dictionary["13"]:
            print "\nThis is the intermediate 4-tuple produced by production 19: ", tuple

    ##Handles production 20: proc --> prochead statlist END
    if production_number == 19:

        ##Retrieve name at s_i2
        s_i2 = semantic_stack[len(semantic_stack) - 3]

        if flags_dictionary["14"]:
            print "\nThis was the Local Variable Symbol Table inside a procedure: ", procedure_symbol_table
   
        ##Destroy local symbol table
        procedure_symbol_table = {}
        local_declared_variable_list = []
        procedure = False

        ##4-tuple
        result = s_i2
        operation = "ENDPROCEDURE"
        operand1 = "-"
        operand2 = "-"
        tuple = (result, operation, operand1, operand2)
        intermediate_code.append(tuple)

        if flags_dictionary["13"]:
            print "\nThis is the intermediate 4-tuple produced by production 20: ", tuple

    ##Handles production 22: prochead --> procname fparmlist }
    if production_number == 21:

        ##4-tuple
        result = "-"
        operation = "ENDFORMALPARAMETERS"
        operand1 = "-"
        operand2 = "-"
        tuple = (result, operation, operand1, operand2)
        intermediate_code.append(tuple)

        if flags_dictionary["13"]:
            print "\nThis is the intermediate 4-tuple produced by production 22: ", tuple

    ##Handles production 23: procname --> PROCEDURE variable
    if production_number == 22:

        ##Insert string at s_i into into symbol table
        variable = semantic_stack[len(semantic_stack) - 1]
        if variable in declared_variable_list:
            print "\nThere has been a variable declaration error!"
            print "The variable ", variable, " has been doubly declared."
            print "It will maintain its first declared value."

        else:
            variable_symbol_table[variable] = [("Type", "PROCEDURE")]
            semantic_stack[len(semantic_stack) - 2] = variable

            if flags_dictionary["15"]:
                print "\nThis is the variable symbol table entry just made: ",variable, variable_symbol_table[variable]      

        ##4-tuple
        result = "-"
        operation = "PROCEDUREBEGIN"
        operand1 = variable
        operand2 = "-"
        tuple = (result, operation, operand1, operand2)
        intermediate_code.append(tuple)

        procedure = True
        procedure_symbol_table = copy.copy(variable_symbol_table)
        local_declared_variable_list = []

        if flags_dictionary["13"]:
            print "\nThis is the intermediate 4-tuple produced by production 23: ", tuple

    ##Handles production 24: null-list --> { }
    if production_number == 23:

        ##4-tuple
        result = "-"
        operation = "NOFORMALPARAMETERS"
        operand1 = "-"
        operand2 = "-"
        tuple = (result, operation, operand1, operand2)
        intermediate_code.append(tuple)

        if flags_dictionary["13"]:
            print "\nThis is the intermediate 4-tuple produced by production 24: ", tuple

    ##Handles production 25: fparmlist --> fparmlist , calltype type variable
    if production_number == 24:
        
        ##Insert string at s_i into local symbol table
        variable = semantic_stack[len(semantic_stack) - 1]
        type = semantic_stack[len(semantic_stack) - 2]        
        calltype = semantic_stack[len(semantic_stack) - 3]
        if variable in local_declared_variable_list:
            print "\nThere has been a variable declaration error!"
            print "The variable ", variable, " has been doubly declared."
            print "It will maintain its first declared value."

        else:
            procedure_symbol_table[variable] = [("Calltype", calltype), ("Type", type), ("Shape", "SCALAR"), ("Size", 1)]
            semantic_stack[len(semantic_stack) - 5] = variable

            if flags_dictionary["15"]:
                print "\nThis is the variable symbol table entry just made: ", variable, procedure_symbol_table[variable]

        ##4-tuple
        result = variable
        operation = "FORMAL" + calltype + "PARAMETERS"
        operand1 = 1
        operand2 = "-"
        tuple = (result, operation, operand1, operand2)
        intermediate_code.append(tuple)

        if flags_dictionary["13"]:
            print "\nThis is the intermediate 4-tuple produced by production 25: ", tuple

    ##Handles production 26: fparmlist -->  fparmlist , calltype type variable integer 
    if production_number == 25:
        
        ##Insert string at s_i1 into local symbol table
        variable = semantic_stack[len(semantic_stack) - 2]
        type = semantic_stack[len(semantic_stack) - 3]        
        calltype = semantic_stack[len(semantic_stack) - 4]
        elements = semantic_stack[len(semantic_stack) - 1]
        if variable in local_declared_variable_list:
            print "\nThere has been a variable declaration error!"
            print "The variable ", variable, " has been doubly declared."
            print "It will maintain its first declared value."

        else:
            procedure_symbol_table[variable] = [("Calltype", calltype), ("Type", type), ("Shape", "VECTOR"), ("Elements", elements)] 
            semantic_stack[len(semantic_stack) - 6] = variable
            
            if flags_dictionary["15"]:
                print "\nThis is the variable symbol table entry just made: ", variable, procedure_symbol_table[variable]

        ##4-tuple
        result = variable
        operation = "FORMAL" + calltype + "PARAMETERS"
        operand1 = 1
        operand2 = "-"
        tuple = (result, operation, operand1, operand2)
        intermediate_code.append(tuple)

        if flags_dictionary["13"]:
            print "\nThis is the intermediate 4-tuple produced by production 26: ", tuple

    ##Handles production 27: fparmlist -->  fparmlist , calltype type variable integer :: integer 
    if production_number == 26:

        ##Insert string at s_i3 into local symbol table
        variable = semantic_stack[len(semantic_stack) - 4]
        rows = semantic_stack[len(semantic_stack) - 3]
        columns = semantic_stack[len(semantic_stack) - 1]
        type = semantic_stack[len(semantic_stack) - 5]
        calltype = semantic_stack[len(semantic_stack) - 6]
        if variable in local_declared_variable_list:
            print "\nThere has been a variable declaration error!"
            print "The variable ", variable, " has been doubly declared."
            print "It will maintain its first declared value."

        else:
            procedure_symbol_table[variable] = [("Calltype", calltype), ("Type", type), ("Shape", "MATRIX"), ("Rows", rows), ("Columns", columns)]
            semantic_stack[len(semantic_stack) - 8] = variable

            if flags_dictionary["15"]:
                print "\nThis is the variable symbol table entry just made: ", variable, procedure_symbol_table[variable]

        ##4-tuple
        result = variable
        operation = "FORMAL" + calltype + "PARAMETERS"
        operand1 = rows
        operand2 = columns
        tuple = (result, operation, operand1, operand2)
        intermediate_code.append(tuple)

        if flags_dictionary["13"]:
            print "\nThis is the intermediate 4-tuple produced by production 27: ", tuple

    ##Handles production 28: fparmlist -->  { calltype type variable
    if production_number == 27:

        ##Insert string at s_i into local symbol table
        variable = semantic_stack[len(semantic_stack) - 1]
        type = semantic_stack[len(semantic_stack) - 2]        
        calltype = semantic_stack[len(semantic_stack) - 3]
        if variable in local_declared_variable_list:
            print "\nThere has been a variable declaration error!"
            print "The variable ", variable, " has been doubly declared."
            print "It will maintain its first declared value."

        else:
            procedure_symbol_table[variable] = [("Calltype", calltype), ("Type", type), ("Shape", "SCALAR"), ("Size", 1)]
            semantic_stack[len(semantic_stack) - 4] = variable

            if flags_dictionary["15"]:
                print "\nThis is the variable symbol table entry just made: ", variable, procedure_symbol_table[variable]

        ##4-tuple
        result = "-"
        operation = "BEGINFORMALPARAMETERS"
        operand1 = "-"
        operand2 = "-"
        tuple = (result, operation, operand1, operand2)
        intermediate_code.append(tuple)
        
        if flags_dictionary["13"]:
            print "\nThis is the first intermediate 4-tuple produced by production 28: ", tuple

        ##4-tuple
        result = variable
        operation = "FORMAL" + calltype + "PARAMETERS"
        operand1 = 1
        operand2 = "-"
        tuple = (result, operation, operand1, operand2)
        intermediate_code.append(tuple)
        
        if flags_dictionary["13"]:
            print "\nThis is the second intermediate 4-tuple produced by production 28: ", tuple

    ##Handles production 29: fparmlist -->  { calltype type variable integer
    if production_number == 28:

        ##Insert string at s_i1 into local symbol table
        variable = semantic_stack[len(semantic_stack) - 2]
        type = semantic_stack[len(semantic_stack) - 3]                            
        calltype = semantic_stack[len(semantic_stack) - 4]
        elements = semantic_stack[len(semantic_stack) - 1]          
        if variable in local_declared_variable_list:
            print "\nThere has been a variable declaration error!"
            print "The variable ", variable, " has been doubly declared."
            print "It will maintain its first declared value."

        else:
            procedure_symbol_table[variable] = [("Calltype", calltype), ("Type", type), ("Shape", "VECTOR"), ("Elements", elements)]
            semantic_stack[len(semantic_stack) - 5] = variable

            if flags_dictionary["15"]:
                print "\nThis is the variable symbol table entry just made: ", variable, procedure_symbol_table[variable]

        ##4-tuple
        result = "-"
        operation = "BEGINFORMALPARAMETERS"
        operand1 = "-"
        operand2 = "-"
        tuple = (result, operation, operand1, operand2)
        intermediate_code.append(tuple)

        if flags_dictionary["13"]:
            print "\nThis is the first intermediate 4-tuple produced by production 29: ", tuple

        ##4-tuple
        result = variable
        operation = "FORMAL" + calltype + "PARAMETERS"
        operand1 = elements
        operand2 = "-"
        tuple = (result, operation, operand1, operand2)
        intermediate_code.append(tuple)

        if flags_dictionary["13"]:
            print "\nThis is the second intermediate 4-tuple produced by production 29: ", tuple

    ##Handles production 30: fparmlist -->  { calltype type variable integer :: integer
    if production_number == 29:

        ##Insert string at s_i3 into local symbol table
        variable = semantic_stack[len(semantic_stack) - 4]
        rows = semantic_stack[len(semantic_stack) - 3]
        columns = semantic_stack[len(semantic_stack) - 1]
        type = semantic_stack[len(semantic_stack) - 5]
        calltype = semantic_stack[len(semantic_stack) - 6]
        if variable in local_declared_variable_list:
            print "\nThere has been a variable declaration error!"
            print "The variable ", variable, " has been doubly declared."
            print "It will maintain its first declared value."

        else:
            procedure_symbol_table[variable] = [("Calltype", calltype), ("Type", type), ("Shape", "MATRIX"), ("Rows", rows), ("Columns", columns)]
            semantic_stack[len(semantic_stack) - 7] = variable

            if flags_dictionary["15"]:
                print "\nThis is the variable symbol table entry just made: ", variable, procedure_symbol_table[variable]            

        ##4-tuple
        result = "-"
        operation = "BEGINFORMALPARAMETERS"
        operand1 = "_"
        operand2 = "-"
        tuple = (result, operation, operand1, operand2)
        intermediate_code.append(tuple)

        if flags_dictionary["13"]:
            print "\nThis is the first intermediate 4-tuple produced by production 30: ", tuple

        ##4-tuple
        result = variable
        operation = "FORMAL" + calltype + "PARAMETERS"
        operand1 = rows
        operand2 = columns
        tuple = (result, operation, operand1, operand2)
        intermediate_code.append(tuple)

        if flags_dictionary["13"]:
            print "\nThis is the second intermediate 4-tuple produced by production 30: ", tuple

    ##Handles production 31: calltype --> VALUE
    if production_number == 30:

        ##Set s_i to "value"
        s_i = len(semantic_stack) - 1
        semantic_stack[s_i] = "VALUE"

    ##Handles production 32: calltype --> REFERENCE
    if production_number == 31:

        ##Set s_i to "reference"
        s_i = len(semantic_stack) - 1
        semantic_stack[s_i] = "REFERENCE"

    ##Handles production 33: execpart --> exechead statlist END
    if production_number == 32:

        ##4-tuple
        result = "-"
        operation = "ENDCOMPUTATION"
        operand1 = "-"
        operand2 = "-"
        tuple = (result, operation, operand1, operand2)
        intermediate_code.append(tuple)

    ##Handles production 34: exechead --> MAIN
    if production_number == 33:

        ##4-tuple
        result = "MAIN"
        operation = "LABEL"
        operand1 = "-"
        operand2 = "-"
        tuple = (result, operation, operand1, operand2)
        intermediate_code.append(tuple)

    ##Handles production 43: inputstat --> inputstat , variable
    if production_number == 42:
        variable = semantic_stack[len(semantic_stack) - 1]

        ##4-tuple
        result = "-"
        operation = "INPUTPARAMETER"
        operand1 = variable
        operand2 = "-"
        tuple = (result, operation, operand1, operand2)
        intermediate_code.append(tuple)
        semantic_stack[len(semantic_stack) - 3] = variable

        if flags_dictionary["13"]:
            print "\nThis is the first intermediate 4-tuple produced by production 43: ", tuple

    ##Handles production 44: inputstat --> inputstat , variable [ aexpr ]
    if production_number == 43:
        variable = semantic_stack[len(semantic_stack) - 4]
        element = semantic_stack[len(semantic_stack) - 2]

        ##4-tuple
        result1 = "-"
        operation = "INPUTPARAMETER"
        operand1 = variable
        operand2 = element
        tuple = (result1, operation, operand1, operand2)
        intermediate_code.append(tuple)
        semantic_stack[len(semantic_stack) - 6] = variable

        if flags_dictionary["13"]:
            print "\nThis is the second intermediate 4-tuple produced by production 44: ", tuple

    ##Handles production 45: inputstat --> inputstat , variable [ aexpr : aexpr ]
    if production_number == 44:
        variable = semantic_stack[len(semantic_stack) - 6]
        aexpr1 = semantic_stack[len(semantic_stack) - 4]
        aexpr2 = semantic_stack[len(semantic_stack) - 2]     
        
        type = GetType.get_type(variable, variable_symbol_table, procedure_symbol_table, inside_procedure)
        type = string.lstrip(type [0])
        columns = GetColumns.get_columns(variable, variable_symbol_table, procedure_symbol_table, inside_procedure)

        ##4-tuple
        key = len(intermediate_code)
        result = type + "$" + str(key)
        operation = type + "MULT"
        operand1 = aexpr1
        operand2 = columns
        tuple = (result, operation, operand1, operand2)
        intermediate_code.append(tuple)

        if flags_dictionary["13"]:
            print "\nThis is the first intermediate 4-tuple produced by production 45: ", tuple

        ##4-tuple
        key = len(intermediate_code)
        result1 = type + "$" + str(key)
        operation = type + "ADD"
        operand1 = result
        operand2 = variable
        tuple = (result1, operation, operand1, operand2)
        intermediate_code.append(tuple)

        if flags_dictionary["13"]:
            print "\nThis is the second intermediate 4-tuple produced by production 45: ", tuple

        ##4-tuple
        result2 = "-"
        operation = "INPUTPARAMETER"
        operand1 = variable
        operand2 = result1
        tuple = (result2, operation, operand1, operand2)
        intermediate_code.append(tuple)
        semantic_stack[len(semantic_stack) - 8] = variable

        if flags_dictionary["13"]:
            print "\nThis is the third intermediate 4-tuple produced by production 45: ", tuple

    ##Handles production 46: inputstat --> INPUT variable
    if production_number == 45:
        variable = semantic_stack[len(semantic_stack) - 1]

        ##4-tuple
        result = "-"
        operation = "CALL"
        operand1 = "scanf"
        operand2 = "-"
        tuple = (result, operation, operand1, operand2)
        intermediate_code.append(tuple)

        if flags_dictionary["13"]:
            print "\nThis is the first intermediate 4-tuple produced by production 46: ", tuple

        ##4-tuple
        result1 = "-"
        operation = "INPUTPARAMETER"
        operand1 = variable
        operand2 = "-"
        tuple = (result1, operation, operand1, operand2)
        intermediate_code.append(tuple)
        semantic_stack[len(semantic_stack) - 2] = variable

        if flags_dictionary["13"]:
            print "\nThis is the second intermediate 4-tuple produced by production 46: ", tuple

    ##Handles production 47: inputstat --> INPUT variable [ aexpr ]
    if production_number == 46:
        variable = semantic_stack[len(semantic_stack) - 4]
        element = semantic_stack[len(semantic_stack) - 2]

        ##4-tuple
        result = "-"
        operation = "CALL"
        operand1 = "scanf"
        operand2 = "-"
        tuple = (result, operation, operand1, operand2)
        intermediate_code.append(tuple)

        if flags_dictionary["13"]:
            print "\nThis is the first intermediate 4-tuple produced by production 47: ", tuple

        ##4-tuple
        result2 = "-"
        operation = "INPUTPARAMETER"
        operand1 = variable
        operand2 = element
        tuple = (result2, operation, operand1, operand2)
        intermediate_code.append(tuple)
        semantic_stack[len(semantic_stack) - 5] = variable

        if flags_dictionary["13"]:
            print "\nThis is the third intermediate 4-tuple produced by production 47: ", tuple

    ##Handles production 48: inputstat --> INPUT variable [ aexpr : aexpr ]
    if production_number == 47:
        variable = semantic_stack[len(semantic_stack) - 6]
        aexpr1 = semantic_stack[len(semantic_stack) - 4]
        aexpr2 = semantic_stack[len(semantic_stack) - 2]        

        type = GetType.get_type(variable, variable_symbol_table, procedure_symbol_table, inside_procedure)
        type = string.lstrip(type [0])
        columns = GetColumns.get_columns(variable, variable_symbol_table, procedure_symbol_table, inside_procedure)

        ##4-tuple
        result = "-"
        operation = "CALL"
        operand1 = "scanf"
        operand2 = "-"
        tuple = (result, operation, operand1, operand2)
        intermediate_code.append(tuple)

        if flags_dictionary["13"]:
            print "\nThis is the first intermediate 4-tuple produced by production 48: ", tuple

        ##4-tuple
        key = len(intermediate_code)
        result1 = type + "$" + str(key)
        operation = type + "MULT"
        operand1 = aexpr1
        operand2 = columns
        tuple = (result1, operation, operand1, operand2)
        intermediate_code.append(tuple)

        if flags_dictionary["13"]:
            print "\nThis is the second intermediate 4-tuple produced by production 48: ", tuple

        ##4-tuple
        key = len(intermediate_code)
        result2 = type + "$" + str(key)
        operation = type + "ADD"
        operand1 = result1
        operand2 = variable
        tuple = (result2, operation, operand1, operand2)
        intermediate_code.append(tuple)

        if flags_dictionary["13"]:
            print "\nThis is the third intermediate 4-tuple produced by production 48: ", tuple

        ##4-tuple
        result3 = "-"
        operation = "INPUTPARAMETER"
        operand1 = variable
        operand2 = result2
        tuple = (result3, operation, operand1, operand2)
        intermediate_code.append(tuple)
        semantic_stack[len(semantic_stack) - 7] = variable

        if flags_dictionary["13"]:
            print "\nThis is the fourth intermediate 4-tuple produced by production 48: ", tuple

    ##Handles production 49: outputstat --> outputstat , variable
    if production_number == 48:  
        variable = semantic_stack[len(semantic_stack) - 1]

        ##4-tuple
        result = "-"
        operation = "OUTPUTPARAMETER"
        operand1 = variable
        operand2 = "-"
        tuple = (result, operation, operand1, operand2)
        intermediate_code.append(tuple)
        semantic_stack[len(semantic_stack) - 3] = variable

        if flags_dictionary["13"]:
            print "\nThis is the first intermediate 4-tuple produced by production 49: ", tuple

    ##Handles production 50: outputstat --> outputstat , constant
    if production_number == 49:
        constant = semantic_stack[len(semantic_stack) - 1]

        ##4-tuple
        result = "-"
        operation = "OUTPUTPARAMETER"
        operand1 = constant
        operand2 = "-"
        tuple = (result, operation, operand1, operand2)
        intermediate_code.append(tuple)
        semantic_stack[len(semantic_stack) - 3] = constant

        if flags_dictionary["13"]:
            print "\nThis is the first intermediate 4-tuple produced by production 50: ", tuple

    ##Handles production 51: outputstat --> outputstat , variable [ aexpr ]
    if production_number == 50:
        variable = semantic_stack[len(semantic_stack) - 4]
        element = semantic_stack[len(semantic_stack) - 2]

        ##4-tuple
        result1 = "-"
        operation = "OUTPUTPARAMETER"
        operand1 = variable
        operand2 = element
        tuple = (result1, operation, operand1, operand2)
        intermediate_code.append(tuple)
        semantic_stack[len(semantic_stack) - 6] = variable

        if flags_dictionary["13"]:
            print "\nThis is the second intermediate 4-tuple produced by production 51: ", tuple

    ##Handles production 52: outputstat --> outputstat , variable [ aexpr : aexpr ]
    if production_number == 51:
        variable = semantic_stack[len(semantic_stack) - 6]
        aexpr1 = semantic_stack[len(semantic_stack) - 4]
        aexpr2 = semantic_stack[len(semantic_stack) - 2]
              
        type = GetType.get_type(variable, variable_symbol_table, procedure_symbol_table, inside_procedure)
        type = string.lstrip(type [0])
        columns = GetColumns.get_columns(variable, variable_symbol_table, procedure_symbol_table, inside_procedure)

        ##4-tuple
        key = len(intermediate_code)
        result = type + "$" + str(key)
        operation = type + "MULT"
        operand1 = aexpr1
        operand2 = columns
        tuple = (result, operation, operand1, operand2)
        intermediate_code.append(tuple)

        if flags_dictionary["13"]:
            print "\nThis is the first intermediate 4-tuple produced by production 52: ", tuple

        ##4-tuple
        key = len(intermediate_code)
        result1 = type + "$" + str(key)
        operation = type + "ADD"
        operand1 = result
        operand2 = variable
        tuple = (result1, operation, operand1, operand2)
        intermediate_code.append(tuple)

        if flags_dictionary["13"]:
            print "\nThis is the second intermediate 4-tuple produced by production 52: ", tuple

        ##4-tuple
        result2 = "-"
        operation = "OUTPUTPARAMETER"
        operand1 = variable
        operand2 = result1
        tuple = (result2, operation, operand1, operand2)
        intermediate_code.append(tuple)
        semantic_stack[len(semantic_stack) - 8] = variable

        if flags_dictionary["13"]:
            print "\nThis is the third intermediate 4-tuple produced by production 52: ", tuple

    ##Handles production 53: outputstat --> OUTPUT variable
    if production_number == 52:
        variable = semantic_stack[len(semantic_stack) - 1]

        ##4-tuple
        result = "-"
        operation = "CALL"
        operand1 = "printf"
        operand2 = "-"
        tuple = (result, operation, operand1, operand2)
        intermediate_code.append(tuple)
        
        if flags_dictionary["13"]:
            print "\nThis is the first intermediate 4-tuple produced by production 53: ", tuple

        ##4-tuple
        result1 = "-"
        operation = "OUTPUTPARAMETER"
        operand1 = variable
        operand2 = "-"
        tuple = (result1, operation, operand1, operand2)
        intermediate_code.append(tuple)
        semantic_stack[len(semantic_stack) - 2] = variable

        if flags_dictionary["13"]:
            print "\nThis is the second intermediate 4-tuple produced by production 53: ", tuple

    ##Handles production 54: outputstat --> OUTPUT constant
    if production_number == 53:
        constant = semantic_stack[len(semantic_stack) - 1]

        ##4-tuple
        result = "-"
        operation = "CALL"
        operand1 = "printf"
        operand2 = "-"
        tuple = (result, operation, operand1, operand2)
        intermediate_code.append(tuple)

        if flags_dictionary["13"]:
            print "\nThis is the first intermediate 4-tuple produced by production 54: ", tuple

        ##4-tuple
        result1 = "-"
        operation = "OUTPUTPARAMETER"
        operand1 = constant
        operand2 = "-"
        tuple = (result1, operation, operand1, operand2)
        intermediate_code.append(tuple)
        semantic_stack[len(semantic_stack) - 2] = constant

        if flags_dictionary["13"]:
            print "\nThis is the second intermediate 4-tuple produced by production 54: ", tuple

    ##Handles production 55: outputstat --> OUTPUT variable [ aexpr ]
    if production_number == 54:
        variable = semantic_stack[len(semantic_stack) - 4]
        element = semantic_stack[len(semantic_stack) - 2]

        type = GetType.get_type(element, variable_symbol_table, procedure_symbol_table, inside_procedure)
        type = string.lstrip(type [0])

        ##4-tuple
        result = "-"
        operation = "CALL"
        operand1 = "printf"
        operand2 = "-"
        tuple = (result, operation, operand1, operand2)
        intermediate_code.append(tuple)

        if flags_dictionary["13"]:
            print "\nThis is the first intermediate 4-tuple produced by production 55: ", tuple

        ##4-tuple
        result2 = "-"
        operation = "OUTPUTPARAMETER"
        operand1 = variable
        operand2 = element
        tuple = (result2, operation, operand1, operand2)
        intermediate_code.append(tuple)
        semantic_stack[len(semantic_stack) - 5] = variable

        if flags_dictionary["13"]:
            print "\nThis is the third intermediate 4-tuple produced by production 56: ", tuple

    ##Handles production 56: outputstat --> OUTPUT variable [aexpr : aexpr]
    if production_number == 55: 
        variable = semantic_stack[len(semantic_stack) - 6]
        aexpr1 = semantic_stack[len(semantic_stack) - 4]
        aexpr2 = semantic_stack[len(semantic_stack) - 2]

        type = GetType.get_type(variable, variable_symbol_table, procedure_symbol_table, inside_procedure)
        type = string.lstrip(type [0])
        columns = GetColumns.get_columns(variable, variable_symbol_table, procedure_symbol_table, inside_procedure)

        ##4-tuple
        result = "-"
        operation = "CALL"
        operand1 = "printf"
        operand2 = "-"
        tuple = (result, operation, operand1, operand2)
        intermediate_code.append(tuple)

        if flags_dictionary["13"]:
            print "\nThis is the first intermediate 4-tuple produced by production 56: ", tuple

        ##4-tuple
        key = len(intermediate_code)
        result1 = type + "$" + str(key)
        operation = type + "MULT"
        operand1 = aexpr1
        operand2 = columns
        tuple = (result1, operation, operand1, operand2)
        intermediate_code.append(tuple)

        if flags_dictionary["13"]:
            print "\nThis is the second intermediate 4-tuple produced by production 56: ", tuple

        ##4-tuple
        key = len(intermediate_code)
        result2 = type + "$" + str(key)
        operation = type + "ADD"
        operand1 = result
        operand2 = variable
        tuple = (result2, operation, operand1, operand2)
        intermediate_code.append(tuple)

        if flags_dictionary["13"]:
            print "\nThis is the third intermediate 4-tuple produced by production 56: ", tuple

        ##4-tuple
        result3 = "-"
        operation = "OUTPUTPARAMETER"
        operand1 = variable
        operand2 = result2
        tuple = (result3, operation, operand1, operand2)
        intermediate_code.append(tuple)
        semantic_stack[len(semantic_stack) - 7] = variable

        if flags_dictionary["13"]:
            print "\nThis is the fourth intermediate 4-tuple produced by production 56: ", tuple

    ##Handles production 57: callstat --> callname null-list
    if production_number == 56:

        ##4-tuple
        result = "-"
        operation = "NOACTUALPARAMETER"
        operand1 = "-"
        operand2 = "-"
        tuple = (result, operation, operand1, operand2)
        intermediate_code.append(tuple)

        if flags_dictionary["13"]:
            print "\nThis is the first intermediate 4-tuple produced by production 57: ", tuple

    ##Handles production 58: callstat --> callname aparmlist
    if production_number == 57:

        ##4-tuple
        result = "-"
        operation = "ENDACTUALPARAMETER"
        operand1 = "-"
        operand2 = "-"
        tuple = (result, operation, operand1, operand2)
        intermediate_code.append(tuple)

        if flags_dictionary["13"]:
            print "\nThis is the first intermediate 4-tuple produced by production 58: ", tuple

    ##Handles production 59: callname --> CALL variable
    if production_number == 58:
        variable = semantic_stack[len(semantic_stack) - 1]

        type = GetType.get_type(variable, variable_symbol_table, procedure_symbol_table, inside_procedure)

        if type != "PROCEDURE":
            print "type Error Found!"
            print "Variable", variable, "Not of type PROCEDURE."

        ##4-tuple
        result = "-"
        operation = "CALL"
        operand1 = variable
        operand2 = "-"
        tuple = (result, operation, operand1, operand2)
        intermediate_code.append(tuple)
        semantic_stack[len(semantic_stack) - 2] = variable

        if flags_dictionary["13"]:
            print "\nThis is the first intermediate 4-tuple produced by production 59: ", tuple

    ##Handles production 60: aparmlist --> aparmlist , calltype variable
    if production_number == 59:        
        variable = semantic_stack[len(semantic_stack) - 1]
        calltype = semantic_stack[len(semantic_stack) - 2]

        ##4-tuple
        result1 = "-"
        operation = calltype + "PARAMETER"
        operand1 = variable
        operand2 = "-"
        tuple = (result1, operation, operand1, operand2)
        intermediate_code.append(tuple)
        semantic_stack[len(semantic_stack) - 4] = variable

        if flags_dictionary["13"]:
            print "\nThis is the first intermediate 4-tuple produced by production 60: ", tuple

    ##Handles production 61: aparmlist --> aparmlist , constant
    if production_number == 60:
        constant = semantic_stack[len(semantic_stack) - 1]

        ##4-tuple
        result = "-"
        operation = "VALUEACTUALPARAMETER"
        operand1 = constant
        operand2 = "-"
        tuple = (result, operation, operand1, operand2)
        intermediate_code.append(tuple)
        semantic_stack[len(semantic_stack) - 3] = constant

        if flags_dictionary["13"]:
            print "\nThis is the first intermediate 4-tuple produced by production 61: ", tuple

    ##Handles production 62: aparmlist --> aparmlist , calltype variable [ aexpr ]
    if production_number == 61:
        variable = semantic_stack[len(semantic_stack) - 4]
        element = semantic_stack[len(semantic_stack) - 2]
        calltype = semantic_stack[len(semantic_stack) - 5]

        type = GetType.get_type(variable, variable_symbol_table, procedure_symbol_table, inside_procedure)
        type = string.lstrip(type [0])

        ##4-tuple
        result = "-"
        operation = "ACTUALPARAMETER"
        operand1 = "-"
        operand2 = "-"
        tuple = (result, operation, operand1, operand2)
        intermediate_code.append(tuple)

        if flags_dictionary["13"]:
            print "\nThis is the first intermediate 4-tuple produced by production 62: ", tuple

        ##4-tuple
        result2 = "-"
        operation = calltype + "PARAMETER"
        operand1 = variable
        operand2 = element
        tuple = (result2, operation, operand1, operand2)
        intermediate_code.append(tuple)
        semantic_stack[len(semantic_stack) - 7] = variable

        if flags_dictionary["13"]:
            print "\nThis is the third intermediate 4-tuple produced by production 62: ", tuple

    ##Handles production 63: aparmlist --> aparmlist , calltype variable [ aexpr : aexpr ]
    if production_number == 62:
        variable = semantic_stack[len(semantic_stack) - 6]
        aexpr1 = semantic_stack[len(semantic_stack) - 4]
        aexpr2 = semantic_stack[len(semantic_stack) - 2]
        calltype = semantic_stack[len(semantic_stack) - 7]

        type = GetType.get_type(variable, variable_symbol_table, procedure_symbol_table, inside_procedure)
        type = string.lstrip(type [0])
        columns = GetColumns.get_columns(variable, variable_symbol_table, procedure_symbol_table, inside_procedure)

        ##4-tuple
        result = "-"
        operation = "ACTUALPARAMETER"
        operand1 = "-"
        operand2 = "-"
        tuple = (result, operation, operand1, operand2)
        intermediate_code.append(tuple)

        if flags_dictionary["13"]:
            print "\nThis is the first intermediate 4-tuple produced by production 63: ", tuple

        ##4-tuple
        key = len(intermediate_code)
        result1 = type + "$" + str(key)
        operation = type + "MULT"
        operand1 = aexpr1
        operand2 = columns
        tuple = (result1, operation, operand1, operand2)
        intermediate_code.append(tuple)

        if flags_dictionary["13"]:
            print "\nThis is the second intermediate 4-tuple produced by production 63: ", tuple

        ##4-tuple
        key = len(intermediate_code)
        result2 = type + "$" + str(key)
        operation = type + "ADD"
        operand1 = result1
        operand2 = variable
        tuple = (result2, operation, operand1, operand2)
        intermediate_code.append(tuple)

        if flags_dictionary["13"]:
            print "\nThis is the third intermediate 4-tuple produced by production 63: ", tuple

        ##4-tuple
        result3 = "-"
        operation = calltype + "PARAMETER"
        operand1 = variable
        operand2 = result2
        tuple = (result3, operation, operand1, operand2)
        intermediate_code.append(tuple)
        semantic_stack[len(semantic_stack) - 9] = variable

        if flags_dictionary["13"]:
            print "\nThis is the fourth intermediate 4-tuple produced by production 63: ", tuple

    ##Handles production 64: aparmlist --> { calltype variable
    if production_number == 63:
        variable = semantic_stack[len(semantic_stack) - 1]
        calltype = semantic_stack[len(semantic_stack) - 2]

        ##4-tuple
        result = "-"
        operation = "BEGINACTUALPARAMETER"
        operand1 = "-"
        operand2 = "-"
        tuple = (result, operation, operand1, operand2)
        intermediate_code.append(tuple)

        if flags_dictionary["13"]:
            print "\nThis is the first intermediate 4-tuple produced by production 64: ", tuple

        ##4-tuple
        result1 = "-"
        operation = calltype + "PARAMETER"
        operand1 = variable
        operand2 = "-"
        tuple = (result1, operation, operand1, operand2)
        intermediate_code.append(tuple)
        semantic_stack[len(semantic_stack) - 3] = variable

        if flags_dictionary["13"]:
            print "\nThis is the second intermediate 4-tuple produced by production 64: ", tuple

    ##Handles production 65: aparmlist --> { constant
    if production_number == 64:
        constant = semantic_stack[len(semantic_stack) - 1]

        ##4-tuple
        result = "-"
        operation = "VALUEACTUALPARAMETER"
        operand1 = constant
        operand2 = "-"
        tuple = (result, operation, operand1, operand2)
        intermediate_code.append(tuple)
        semantic_stack[len(semantic_stack) - 2] = constant

        if flags_dictionary["13"]:
            print "\nThis is the first intermediate 4-tuple produced by production 65: ", tuple

    ##Handles production 66: aparmlist --> { calltype variable [ aexpr ]
    if production_number == 65:
        variable = semantic_stack[len(semantic_stack) - 4]
        element = semantic_stack[len(semantic_stack) - 2]
        calltype = semantic_stack[len(semantic_stack) - 5]

        type = GetType.get_type(variable, variable_symbol_table, procedure_symbol_table, inside_procedure)
        type = string.lstrip(type [0])
        elements = GetElements.get_elements(variable, variable_symbol_table, procedure_symbol_table, inside_procedure)

        ##4-tuple
        result = "-"
        operation = "BEGINACTUALPARAMETER"
        operand1 = "-"
        operand2 = "-"
        tuple = (result, operation, operand1, operand2)
        intermediate_code.append(tuple)

        if flags_dictionary["13"]:
            print "\nThis is the first intermediate 4-tuple produced by production 66: ", tuple

        ##4-tuple
        result2 = "-"
        operation = calltype + "PARAMETER"
        operand1 = variable
        operand2 = element
        tuple = (result2, operation, operand1, operand2)
        intermediate_code.append(tuple)
        semantic_stack[len(semantic_stack) - 6] = variable

        if flags_dictionary["13"]:
            print "\nThis is the third intermediate 4-tuple produced by production 66: ", tuple

    ##Handles production 67: aparmlist --> { calltype variable [ aexpr : aexpr ]
    if production_number == 66:
        variable = semantic_stack[len(semantic_stack) - 6]
        aexpr1 = semantic_stack[len(semantic_stack) - 4]
        aexpr2 = semantic_stack[len(semantic_stack) - 2]

        calltype = semantic_stack[len(semantic_stack) - 7]

        type = GetType.get_type(rows, variable_symbol_table, procedure_symbol_table, inside_procedure)
        type = string.lstrip(type [0])

        ##4-tuple
        result = "-"
        operation = "BEGINACTUALPARAMETER"
        operand1 = "-"
        operand2 = "-"
        tuple = (result, operation, operand1, operand2)
        intermediate_code.append(tuple)

        if flags_dictionary["13"]:
            print "\nThis is the first intermediate 4-tuple produced by production 67: ", tuple

        ##4-tuple
        key = len(intermediate_code)
        result1 = type + "$" + str(key)
        operation = type + "MULT"
        operand1 = aexpr1
        operand2 = columns
        tuple = (result1, operation, operand1, operand2)
        intermediate_code.append(tuple)

        if flags_dictionary["13"]:
            print "\nThis is the second intermediate 4-tuple produced by production 67: ", tuple

        ##4-tuple
        key = len(intermediate_code)
        result2 = type + "$" + str(key)
        operation = type + "ADD"
        operand1 = result1
        operand2 = variable
        tuple = (result2, operation, operand1, operand2)
        intermediate_code.append(tuple)

        if flags_dictionary["13"]:
            print "\nThis is the third intermediate 4-tuple produced by production 67: ", tuple

        ##4-tuple
        result3 = "-"
        operation = calltype + "PARAMETER"
        operand1 = variable
        operand2 = result2
        tuple = (result3, operation, operand1, operand2)
        intermediate_code.append(tuple)
        semantic_stack[len(semantic_stack) - 8] = variable

        if flags_dictionary["13"]:
            print "\nThis is the fourth intermediate 4-tuple produced by production 67: ", tuple

    ##Handles production 68: ifstat --> ifhead statlist END
    if production_number == 67:
        label = semantic_stack[len(semantic_stack) - 3]

        ##4-tuple
        result = label
        operation = "LABEL"
        operand1 = "-"
        operand2 = "-"
        tuple = (result, operation, operand1, operand2)
        intermediate_code.append(tuple)
        semantic_stack[len(semantic_stack) - 3] = result

        if flags_dictionary["13"]:
            print "\nThis is the first intermediate 4-tuple produced by production 68: ", tuple

    ##Handles production 69: ifstat --> ifthen statlist END
    if production_number == 68:
        label = semantic_stack[len(semantic_stack) - 3]

        ##4-tuple
        result = label
        operation = "LABEL"
        operand1 = "-"
        operand2 = "-"
        tuple = (result, operation, operand1, operand2)
        intermediate_code.append(tuple)
        semantic_stack[len(semantic_stack) - 3] = result

        if flags_dictionary["13"]:
            print "\nThis is the first intermediate 4-tuple produced by production 69: ", tuple

    ##Handles production 70: ifthen --> ifhead statlist ELSE
    if production_number == 69:
        label = semantic_stack[len(semantic_stack) - 3]
        variable = semantic_stack[len(semantic_stack) - 2]

        label1 = string.rsplit(label [2:])
        label2 = int(label1[0]) + 1
        label = "L$" + str(label2)

        ##4-tuple
        key = len(intermediate_code)
        result = label
        operation = "JUMP"
        operand1 = "-"
        operand2 = "-"
        tuple = (result, operation, operand1, operand2)
        intermediate_code.append(tuple)
        semantic_stack[len(semantic_stack) - 3] = label

        if flags_dictionary["13"]:
            print "\nThis is the first intermediate 4-tuple produced by production 70: ", tuple

    ##Handles production 71: ifhead --> IF ( bexpr ) THEN
    if production_number == 70:
        variable = semantic_stack[len(semantic_stack) - 3]

        key = len(intermediate_code)
        label1 = "L$" + str(key)     

        ##4-tuple
        result = label1
        operation = "CJUMPF"
        operand1 = variable
        operand2 = "-"
        tuple = (result, operation, operand1, operand2)
        intermediate_code.append(tuple)
        semantic_stack[len(semantic_stack) - 5] = label1
        
        if flags_dictionary["13"]:
            print "\nThis is the first intermediate 4-tuple produced by production 71: ", tuple

    ##Handles production 72: forstat --> forcond statlist INCREMENT variable BY aexpr END
    if production_number == 71:
        variable = semantic_stack[len(semantic_stack) - 4]
        aexpr = semantic_stack[len(semantic_stack) - 2]
        label = semantic_stack[len(semantic_stack) - 7]

        type = GetType.get_type(variable, variable_symbol_table, procedure_symbol_table, inside_procedure)
        type = string.lstrip(type [0])

        label1 = string.rsplit(label [2:])
        label2 = int(label1[0]) + 1
        label2 = "L$" + str(label2)

        ##4-tuple
        result = label2
        operation = "LABEL"
        operand1 = "-"
        operand2 = "-"
        tuple = (result, operation, operand1, operand2)
        intermediate_code.append(tuple)
        semantic_stack[len(semantic_stack) - 7] = label2

        if flags_dictionary["13"]:
            print "\nThis is the first intermediate 4-tuple produced by production 72: ", tuple

        ##4-tuple
        result = variable
        operation = type + "ADD"
        operand1 = variable
        operand2 = aexpr
        tuple = (result, operation, operand1, operand2)
        intermediate_code.append(tuple)

        if flags_dictionary["13"]:
            print "\nThis is the second intermediate 4-tuple produced by production 72: ", tuple   

        ##4-tuple
        key = len(intermediate_code)
        result = label
        operation = "JUMP"
        operand1 = "-"
        operand2 = "-"
        tuple = (result, operation, operand1, operand2)
        intermediate_code.append(tuple)

        if flags_dictionary["13"]:
            print "\nThis is the third intermediate 4-tuple produced by production 72: ", tuple  

    ##Handles production 73: forcond --> forhead ( bexpr ) DO
    if production_number == 72:
        bexpr = semantic_stack[len(semantic_stack) - 3]
        old_label = semantic_stack[len(semantic_stack) - 5]

        key = len(intermediate_code)
        label1 = "L$" + str(key)
        label2 = "L$" + str(key + 1)

        ##4-tuple
        result = label1
        operation = "LABEL"
        operand1 = "-"
        operand2 = "-"
        tuple = (result, operation, operand1, operand2)
        intermediate_code.append(tuple)
        semantic_stack[len(semantic_stack) - 5] = label1

        if flags_dictionary["13"]:
            print "\nThis is the first intermediate 4-tuple produced by production 73: ", tuple

        ##4-tuple
        key = len(intermediate_code)
        result = label2
        operation = "CJUMP"
        operand1 = bexpr
        operand2 = "-"
        tuple = (result, operation, operand1, operand2)
        intermediate_code.append(tuple)

        if flags_dictionary["13"]:
            print "\nThis is the second intermediate 4-tuple produced by production 73: ", tuple

    ##Handles production 74: forhead --> FOR variable <_ aexpr UNTIL
    if production_number == 73:
        variable = semantic_stack[len(semantic_stack) - 4]
        aexpr = semantic_stack[len(semantic_stack) - 2]

        type = GetType.get_type(variable, variable_symbol_table, procedure_symbol_table, inside_procedure)
        type = string.lstrip(type [0])

        ##4-tuple
        result = variable
        operation = "SUBSTORE"
        operand1 = aexpr
        operand2 = "-"
        tuple = (result, operation, operand1, operand2)
        intermediate_code.append(tuple)
        semantic_stack[len(semantic_stack) - 3] = aexpr

        if flags_dictionary["13"]:
            print "\nThis is the first intermediate 4-tuple produced by production 74: ", tuple

    ##Handles production 76: astat --> variable <_ aexpr
    if production_number == 75:
        variable = semantic_stack[len(semantic_stack) - 3]
        aexpr = semantic_stack[len(semantic_stack) - 1]

        type = GetType.get_type(variable, variable_symbol_table, procedure_symbol_table, inside_procedure)
        type = string.lstrip(type [0])

        ##4-tuple
        result = variable
        operation = "SUBSTORE"
        operand1 = aexpr
        operand2 = "-"
        tuple = (result, operation, operand1, operand2)
        intermediate_code.append(tuple)
        semantic_stack[len(semantic_stack) - 3] = aexpr

        if flags_dictionary["13"]:
            print "\nThis is the first intermediate 4-tuple produced by production 76: ", tuple

    ##Handles production 77: astat --> variable [ aexpr ] <_ aexpr
    if production_number == 76:
        variable = semantic_stack[len(semantic_stack) - 6]
        element = semantic_stack[len(semantic_stack) - 4]
        aexpr = semantic_stack[len(semantic_stack) - 1]

        ##4-tuple
        result1 = variable
        operation = "SUBSTORE"
        operand1 = element
        operand2 = aexpr
        tuple = (result1, operation, operand1, operand2)
        intermediate_code.append(tuple)
        semantic_stack[len(semantic_stack) - 6] = aexpr

        if flags_dictionary["13"]:
            print "\nThis is the first intermediate 4-tuple produced by production 77: ", tuple

    ##Handles production 78: astat --> variable [ aexpr : aexpr ] <_ aexpr
    if production_number == 77:
        variable = semantic_stack[len(semantic_stack) - 8]
        aexpr = semantic_stack[len(semantic_stack) - 1]
        aexpr1 = semantic_stack[len(semantic_stack) - 6]
        aexpr2 = semantic_stack[len(semantic_stack) - 4]

        type = GetType.get_type(variable, variable_symbol_table, procedure_symbol_table, inside_procedure)
        type = string.lstrip(type [0])
        columns = GetColumns.get_columns(variable, variable_symbol_table, procedure_symbol_table, inside_procedure)

        ##4-tuple
        key = len(intermediate_code)
        result = type + "$" + str(key)
        operation = type + "MULT"
        operand1 = aexpr1
        operand2 = columns
        tuple = (result, operation, operand1, operand2)
        intermediate_code.append(tuple)

        if flags_dictionary["13"]:
            print "\nThis is the first intermediate 4-tuple produced by production 78: ", tuple

        ##4-tuple
        key = len(intermediate_code)
        result1 = type + "$" + str(key)
        operation = type + "ADD"
        operand1 = result
        operand2 = variable
        tuple = (result1, operation, operand1, operand2)
        intermediate_code.append(tuple)

        if flags_dictionary["13"]:
            print "\nThis is the second intermediate 4-tuple produced by production 78: ", tuple

        ##4-tuple
        result2 = variable
        operation = "SUBSTORE"
        operand1 = aexpr
        operand2 = result1
        tuple = (result2, operation, operand1, operand2)
        intermediate_code.append(tuple)
        semantic_stack[len(semantic_stack) - 8] = aexpr

        if flags_dictionary["13"]:
            print "\nThis is the third intermediate 4-tuple produced by production 78: ", tuple

    ##Handles production 79: andexpr --> bexpr || andexpr
    if production_number == 78:
        bexpr = semantic_stack[len(semantic_stack) - 3]
        andexpr = semantic_stack[len(semantic_stack) - 1]

        ##4-tuple
        key = len(intermediate_code)
        result = "B$" + str(key)
        operation = "OR"
        operand1 = bexpr
        operand2 = andexpr
        tuple = (result, operation, operand1, operand2)
        intermediate_code.append(tuple)
        semantic_stack[len(semantic_stack) - 3] = result   

        if flags_dictionary["13"]:
            print "\nThis is the first intermediate 4-tuple produced by production 79: ", tuple

    ##Handles production 81: andexpr --> andexpr && notexpr
    if production_number == 80:
        andexpr = semantic_stack[len(semantic_stack) - 3]
        notexpr = semantic_stack[len(semantic_stack) - 1]

        ##4-tuple
        key = len(intermediate_code)
        result = "B$" + str(key)
        operation = "AND"
        operand1 = andexpr
        operand2 = notexpr
        tuple = (result, operation, operand1, operand2)
        intermediate_code.append(tuple)
        semantic_stack[len(semantic_stack) - 3] = result

        if flags_dictionary["13"]:
            print "\nThis is the first intermediate 4-tuple produced by production 81: ", tuple

    ##Handles production 83: notexpr --> ! relexpr
    if production_number == 82:
        relexpr = semantic_stack[len(semantic_stack) - 1]

        ##4-tuple
        key = len(intermediate_code)
        result = "B$" + str(key)
        operation = "NOT"
        operand1 = relexpr
        operand2 = "-"
        tuple = (result, operation, operand1, operand2)
        intermediate_code.append(tuple)
        semantic_stack[len(semantic_stack) - 2] = result

        if flags_dictionary["13"]:
            print "\nThis is the first intermediate 4-tuple produced by production 83: ", tuple

    ##Handles production 85: relexpr --> aexpr < aexpr
    if production_number == 84:
        aexpr1 = semantic_stack[len(semantic_stack) - 3]
        aexpr2 = semantic_stack[len(semantic_stack) - 1]

        ##4-tuple
        key = len(intermediate_code)
        result = "B$" + str(key)
        operation = "LESSTHAN"
        operand1 = aexpr1
        operand2 = aexpr2
        tuple = (result, operation, operand1, operand2)
        intermediate_code.append(tuple)
        semantic_stack[len(semantic_stack) - 3] = result

        if flags_dictionary["13"]:
            print "\nThis is the first intermediate 4-tuple produced by production 85: ", tuple

    ##Handles production 86: relexpr --> aexpr <= aexpr
    if production_number == 85:
        aexpr1 = semantic_stack[len(semantic_stack) - 3]
        aexpr2 = semantic_stack[len(semantic_stack) - 1]

        ##4-tuple
        key = len(intermediate_code)
        result = "B$" + str(key)
        operation = "LESSTHANEQUALTO"
        operand1 = aexpr1
        operand2 = aexpr2
        tuple = (result, operation, operand1, operand2)
        intermediate_code.append(tuple)
        semantic_stack[len(semantic_stack) - 3] = result

        if flags_dictionary["13"]:
            print "\nThis is the first intermediate 4-tuple produced by production 86: ", tuple

    ##Handles production 87: relexpr --> aexpr > aexpr
    if production_number == 86:
        aexpr1 = semantic_stack[len(semantic_stack) - 3]
        aexpr2 = semantic_stack[len(semantic_stack) - 1]

        ##4-tuple
        key = len(intermediate_code)
        result = "B$" + str(key)
        operation = "GREATERTHAN"
        operand1 = aexpr1
        operand2 = aexpr2
        tuple = (result, operation, operand1, operand2)
        intermediate_code.append(tuple)
        semantic_stack[len(semantic_stack) - 3] = result

        if flags_dictionary["13"]:
            print "\nThis is the first intermediate 4-tuple produced by production 87: ", tuple

    ##Handles production 88: relexpr --> aexpr >= aexpr
    if production_number == 87:
        aexpr1 = semantic_stack[len(semantic_stack) - 3]
        aexpr2 = semantic_stack[len(semantic_stack) - 1]

        ##4-tuple
        key = len(intermediate_code)
        result = "B$" + str(key)
        operation = "GREATERTHANEQUALTO"
        operand1 = aexpr1
        operand2 = aexpr2
        tuple = (result, operation, operand1, operand2)
        intermediate_code.append(tuple)
        semantic_stack[len(semantic_stack) - 3] = result 

        if flags_dictionary["13"]:
            print "\nThis is the first intermediate 4-tuple produced by production 88: ", tuple

    ##Handles production 89: relexpr --> aexpr == aexpr
    if production_number == 88:
        aexpr1 = semantic_stack[len(semantic_stack) - 3]
        aexpr2 = semantic_stack[len(semantic_stack) - 1]

        ##4-tuple
        key = len(intermediate_code)
        result = "B$" + str(key)
        operation = "EQUAL"
        operand1 = aexpr1
        operand2 = aexpr2
        tuple = (result, operation, operand1, operand2)
        intermediate_code.append(tuple)
        semantic_stack[len(semantic_stack) - 3] = result

        if flags_dictionary["13"]:
            print "\nThis is the first intermediate 4-tuple produced by production 89: ", tuple

    ##Handles production 90: relexpr --> aexpr != aexpr
    if production_number == 89:
        aexpr1 = semantic_stack[len(semantic_stack) - 3]
        aexpr2 = semantic_stack[len(semantic_stack) - 1]

        ##4-tuple
        key = len(intermediate_code)
        result = "B$" + str(key)
        operation = "NOTEQUAL"
        operand1 = aexpr1
        operand2 = aexpr2
        tuple = (result, operation, operand1, operand2)
        intermediate_code.append(tuple)
        semantic_stack[len(semantic_stack) - 3] = result 

        if flags_dictionary["13"]:
            print "\nThis is the first intermediate 4-tuple produced by production 90: ", tuple

    ##Handles production 92: aexpr --> aexpr + term
    if production_number == 91:
        aexpr = semantic_stack[len(semantic_stack) - 3]
        term = semantic_stack[len(semantic_stack) - 1]

        type = GetType.get_type(term, variable_symbol_table, procedure_symbol_table, inside_procedure)
        type = string.lstrip(type [0])

        ##4-tuple
        key = len(intermediate_code)
        result = type + "$" + str(key)
        operation = type + "ADD"
        operand1 = aexpr
        operand2 = term
        tuple = (result, operation, operand1, operand2)
        intermediate_code.append(tuple)
        semantic_stack[len(semantic_stack) - 3] = result

        if flags_dictionary["13"]:
            print "\nThis is the first intermediate 4-tuple produced by production 92: ", tuple

    ##Handles production 93: aexpr --> aexpr - term
    if production_number == 92:
        aexpr = semantic_stack[len(semantic_stack) - 3]
        term = semantic_stack[len(semantic_stack) - 1]

        type = GetType.get_type(term, variable_symbol_table, procedure_symbol_table, inside_procedure)
        type = string.lstrip(type [0])

        ##4-tuple
        key = len(intermediate_code)
        result = type + "$" + str(key)
        operation = type + "SUB"
        operand1 = aexpr
        operand2 = term
        tuple = (result, operation, operand1, operand2)
        intermediate_code.append(tuple)
        semantic_stack[len(semantic_stack) - 3] = result

        if flags_dictionary["13"]:
            print "\nThis is the first intermediate 4-tuple produced by production 93: ", tuple

    ##Handles production 94: aexpr --> - term
    if production_number == 93:
        term = semantic_stack[len(semantic_stack) - 1]

        type = GetType.get_type(term, variable_symbol_table, procedure_symbol_table, inside_procedure)
        type = string.lstrip(type [0])

        ##4-tuple
        key = len(intermediate_code)
        result = type + "$" + str(key)
        operation = type + "SUB"
        operand1 = 0
        operand2 = term
        tuple = (result, operation, operand1, operand2)
        intermediate_code.append(tuple)
        semantic_stack[len(semantic_stack) - 2] = result

        if flags_dictionary["13"]:
            print "\nThis is the first intermediate 4-tuple produced by production 94: ", tuple

    ##Handles production 96: term --> term * primary
    if production_number == 95:
        term = semantic_stack[len(semantic_stack) - 3]
        primary = semantic_stack[len(semantic_stack) - 1]

        type = GetType.get_type(term, variable_symbol_table, procedure_symbol_table, inside_procedure)
        type = string.lstrip(type [0])

        ##4-tuple
        key = len(intermediate_code)
        result = type + "$" + str(key)
        operation = type + "MULT"
        operand1 = term
        operand2 = primary
        tuple = (result, operation, operand1, operand2)
        intermediate_code.append(tuple)
        semantic_stack[len(semantic_stack) - 3] = result

        if flags_dictionary["13"]:
            print "\nThis is the first intermediate 4-tuple produced by production 96: ", tuple

    ##Handles production 97: term --> term / primary
    if production_number == 96:
        term = semantic_stack[len(semantic_stack) - 3]
        primary = semantic_stack[len(semantic_stack) - 1]

        type = GetType.get_type(term, variable_symbol_table, procedure_symbol_table, inside_procedure)
        type = string.lstrip(type [0])

        ##4-tuple
        key = len(intermediate_code)
        result = type + "$" + str(key)
        operation = type + "DIV"
        operand1 = term
        operand2 = primary
        tuple = (result, operation, operand1, operand2)
        intermediate_code.append(tuple)
        semantic_stack[len(semantic_stack) - 3] = result

        if flags_dictionary["13"]:
            print "\nThis is the first intermediate 4-tuple produced by production 97: ", tuple

    ##Handles production 99: primary --> ( bexpr )
    if production_number == 98:
        bexpr = semantic_stack[len(semantic_stack) - 2]

        ##4-tuple
        result = bexpr
        operation = "STORE"
        operand1 = bexpr
        operand2 = "-"
        tuple = (result, operation, operand1, operand2)
        intermediate_code.append(tuple)
        semantic_stack[len(semantic_stack) - 3] = bexpr

        if flags_dictionary["13"]:
            print "\nThis is the first intermediate 4-tuple produced by production 99: ", tuple

    ##Handles production 101: primary --> variable
    if production_number == 100:
        variable = semantic_stack[len(semantic_stack) - 1]

        ##4-tuple
        result = variable
        operation = "SUBLOAD"
        operand1 = variable
        operand2 = "-"
        tuple = (result, operation, operand1, operand2)
        intermediate_code.append(tuple)

        semantic_stack[len(semantic_stack) - 1] = variable

        if flags_dictionary["13"]:
            print "\nThis is the first intermediate 4-tuple produced by production 101: ", tuple

    ##Handles production 102: primary --> variable [ aexpr ]
    if production_number == 101:
        variable = semantic_stack[len(semantic_stack) - 4]
        element = semantic_stack[len(semantic_stack) - 2]         

        ##4-tuple
        key = len(intermediate_code)
        result1 = variable
        operation = "SUBLOAD"
        operand1 = variable
        operand2 = element
        tuple = (result1, operation, operand1, operand2)
        intermediate_code.append(tuple)
        semantic_stack[len(semantic_stack) - 4] = variable

        if flags_dictionary["13"]:
            print "\nThis is the first intermediate 4-tuple produced by production 102: ", tuple

    ##Handles production 103: primary --> variable [ aexpr : aexpr ]
    if production_number == 102:
        variable = semantic_stack[len(semantic_stack) - 6]
        aexpr1 = semantic_stack[len(semantic_stack) - 4]
        aexpr2 = semantic_stack[len(semantic_stack) - 2]     

        type = GetType.get_type(variable, variable_symbol_table, procedure_symbol_table, inside_procedure)
        type = string.lstrip(type [0])
        columns = GetColumns.get_columns(variable, variable_symbol_table, procedure_symbol_table, inside_procedure)               

        ##4-tuple
        key = len(intermediate_code)
        result = type + "$" + str(key)
        operation = type + "MULT"
        operand1 = aexpr1
        operand2 = columns
        tuple = (result, operation, operand1, operand2)
        intermediate_code.append(tuple)

        if flags_dictionary["13"]:
            print "\nThis is the first intermediate 4-tuple produced by production 103: ", tuple

        ##4-tuple
        key = len(intermediate_code)
        result1 = type + "$" + str(key)
        operation = type + "ADD"
        operand1 = result
        operand2 = variable
        tuple = (result1, operation, operand1, operand2)
        intermediate_code.append(tuple)

        if flags_dictionary["13"]:
            print "\nThis is the second intermediate 4-tuple produced by production 103: ", tuple

        ##4-tuple
        key = len(intermediate_code)
        result2 = type + "$" + str(key)
        operation = "SUBLOAD"
        operand1 = variable
        operand2 = result1
        tuple = (result2, operation, operand1, operand2)
        intermediate_code.append(tuple)
        semantic_stack[len(semantic_stack) - 6] = result2

        if flags_dictionary["13"]:
            print "\nThis is the third intermediate 4-tuple produced by production 103: ", tuple

    ##Handles production 104: constant --> integer
    if production_number == 103:
        integer = semantic_stack[len(semantic_stack) - 1]

        ##Insert string at s_i into into symbol table
        if inside_procedure == False:
            attribute = "INTEGER"
            variable_symbol_table[integer] = [("Type", attribute)]
            if flags_dictionary["15"]:
                print "\nThis is the variable symbol table entry just made: ", integer, variable_symbol_table[integer]
        else:
            attribute = "INTEGER"
            procedure_symbol_table[integer] = [("Type", attribute)]
            if flags_dictionary["15"]:
                print "\nThis is the variable symbol table entry just made: ", integer, procedure_symbol_table[integer]

        ##4-tuple
        result = "-"
        operation = "STORECONSTANT"
        operand1 = integer
        operand2 = attribute
        tuple = (result, operation, operand1, operand2)
        intermediate_code.append(tuple)

        if flags_dictionary["13"]:
            print "\nThis is the first intermediate 4-tuple produced by production 104: ", tuple                

        semantic_stack[len(semantic_stack) - 1] = integer

    ##Handles production 105: constant --> real
    if production_number == 104:
        real = semantic_stack[len(semantic_stack) - 1]

        ##Insert string at s_i into into symbol table
        if inside_procedure == False:
            attribute = "REAL"
            variable_symbol_table[real] = [("Type", attribute)]
            if flags_dictionary["15"]:
                print "\nThis is the variable symbol table entry just made: ", real, variable_symbol_table[real]
        else:
            attribute = "REAL"
            procedure_symbol_table[real] = [("Type", attribute)]
            if flags_dictionary["15"]:
                print "\nThis is the variable symbol table entry just made: ", real, procedure_symbol_table[real]

        ##4-tuple
        result = "-"
        operation = "STORECONSTANT"
        operand1 = real
        operand2 = attribute
        tuple = (result, operation, operand1, operand2)
        intermediate_code.append(tuple)

        if flags_dictionary["13"]:
            print "\nThis is the first intermediate 4-tuple produced by production 105: ", tuple

        semantic_stack[len(semantic_stack) - 1] = real

    return semantic_stack, variable_symbol_table, procedure_symbol_table, inside_procedure, intermediate_code, declared_variable_list, local_declared_variable_list, label_list

if __name__ == analyze:
    analyze()
