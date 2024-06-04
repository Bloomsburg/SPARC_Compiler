## Sean Bloomsburg
## sbloomsburg@gmail.com
##
## This module parses the tokens according to
## the grammar returned by the GrammarAnalyzer.
##

import copy
import GrammarAnalyzer
import SemanticAnalyzer


def parse( token, parse_stack, flags_dictionary, character_pair_error, reductions, variable_symbol_table, semantic_stack, procedure_symbol_table, inside_procedure, intermediate_code, declared_variable_list, local_declared_variable_list, label_list):
    ## Imports the pertinent information from the grammar analysis
    variable_dictionary, productions, relation_matrix = GrammarAnalyzer.analyze()
    reverse_variable_dictionary = dict( zip( variable_dictionary.values(), variable_dictionary.keys() ) )

    input_symbol_list = []
    semantic_symbol_list = []

    input_symbol = ''
    parse_symbol = ''

    ## Finds the proper parts of the token created by the lexical analyzer
    ## to be used by the parser
    input_symbol_list.append(token[0])
    semantic_symbol_list.append(token[1])

    if parse_stack[len(parse_stack) - 1] == '$':
        parse_stack.append(input_symbol_list.pop(0))

    if semantic_stack[len(semantic_stack) - 1] == '$':
        semantic_stack.append(semantic_symbol_list.pop(0))

    ## The symbols from the top of the parser stack and and the input stack are used
    ## to find the relation in the precedence matrix
    if parse_stack[len(parse_stack) - 1] != '$':
        parse_symbol = variable_dictionary[parse_stack[len(parse_stack) - 1]]

    if input_symbol_list != []:
        input_symbol = variable_dictionary[input_symbol_list.pop(0)]
    else:
        input_symbol = ''

    if input_symbol != '':
        row = parse_symbol - 1
        column = input_symbol - 1
        relation = relation_matrix[row][column]
        if flags_dictionary["9"]:
            print "The top of the stack is: ", reverse_variable_dictionary[parse_symbol]
            print "The input symbol is: ", reverse_variable_dictionary[input_symbol]
            if relation == '0':
                symbol_relation = "No relation"
            if relation == '1':
                symbol_relation = "="
            if relation == '2':
                symbol_relation = ">"
            if relation == '3':
                symbol_relation = "<"
            print "The relation is :", symbol_relation, "\n"

        ## Checks to see what the relation is according to the precedence matrix and
        ## determines a course of action
        if relation == '0':
            if character_pair_error != True:
                print "Character pair error between ", reverse_variable_dictionary[parse_symbol], "and ", reverse_variable_dictionary[input_symbol],"\n"

            parse_stack.append(reverse_variable_dictionary[input_symbol])
            semantic_stack.append(semantic_symbol_list.pop(0))
            character_pair_error = True
            return parse_stack, character_pair_error, reductions, variable_symbol_table, semantic_stack, procedure_symbol_table, inside_procedure, intermediate_code, declared_variable_list, local_declared_variable_list, label_list

        if relation == '1':
            if character_pair_error != True:
                parse_stack.append(reverse_variable_dictionary[input_symbol])
                semantic_stack.append(semantic_symbol_list.pop(0))
                return parse_stack, character_pair_error, reductions, variable_symbol_table, semantic_stack, procedure_symbol_table, inside_procedure, intermediate_code, declared_variable_list, local_declared_variable_list, label_list

        if relation == '3':
            if character_pair_error != True:
                parse_stack.append(reverse_variable_dictionary[input_symbol])
                semantic_stack.append(semantic_symbol_list.pop(0))
                return parse_stack, character_pair_error, reductions, variable_symbol_table, semantic_stack, procedure_symbol_table, inside_procedure, intermediate_code, declared_variable_list, local_declared_variable_list, label_list

        if relation == '4':
            if character_pair_error != True:
                parse_stack.append(reverse_variable_dictionary[input_symbol])
                semantic_stack.append(semantic_symbol_list.pop(0))
                return parse_stack, character_pair_error, reductions, variable_symbol_table, semantic_stack, procedure_symbol_table, inside_procedure, intermediate_code, declared_variable_list, local_declared_variable_list, label_list

        if relation == '2':

            ## A '>' has been found indicating a character pair error
            ## this section ends it
            if character_pair_error == True:
                parse_stack.pop(len(parse_stack) - 1)
                semantic_stack.pop(len(semantic_stack) - 1)
                top_symbol = variable_dictionary[parse_stack[len(parse_stack) - 1]]
                next_symbol = variable_dictionary[parse_stack[len(parse_stack) - 2]]
                row = next_symbol - 1
                column = top_symbol - 1
                relation = relation_matrix[row][column]

                while relation != '3':
                    parse_stack.pop(len(parse_stack) - 1)
                    semantic_stack.pop(len(semantic_stack) - 1)
                    top_symbol = variable_dictionary[parse_stack[len(parse_stack) - 1]]
                    next_symbol = variable_dictionary[parse_stack[len(parse_stack) - 2]]
                    row = next_symbol - 1
                    column = top_symbol - 1
                    relation = relation_matrix[row][column]

                parse_stack.pop(len(parse_stack) - 1)
                semantic_stack.pop(len(semantic_stack) - 1)
                character_pair_error = False

            ## This section begins the reduction by matching the longest right hand side of
            ## a production to a left hand side
            handle_length = len(parse_stack) - 1
            handle = []
            for i in range(handle_length):
                handle.append(variable_dictionary[parse_stack[i + 1]])

            match = False
            while match != True:

                for i in range(len(productions)):
                    
                    if int(productions[i][0]) == handle_length:
                        raw_potential_match = productions[i]
                        potential_match = []
                        production_number = i
                        
                        for i in range(len(raw_potential_match)):
                            potential_match.append(int(raw_potential_match[i]))

                        potential_match.pop(0)
                        left_hand_side = potential_match.pop(len(potential_match) - 1)
                        
                        ## This section checks for reducibility errors and handles them if necessary.
                        if len(potential_match) != handle_length:
                            lost_handle = []
                            lost_handle.append(parse_stack.pop(len(parse_stack) - 1))
                            top_symbol = variable_dictionary[parse_stack[len(parse_stack) - 1]]
                            next_symbol = variable_dictionary[parse_stack[len(parse_stack) - 2]]
                            row = next_symbol - 1
                            column = top_symbol - 1
                            relation = relation_matrix[row][column]

                            while relation != '3':
                                lost_handle.append(parse_stack.pop(len(parse_stack) - 1))
                                top_symbol = variable_dictionary[parse_stack[len(parse_stack) - 1]]
                                next_symbol = variable_dictionary[parse_stack[len(parse_stack) - 2]]
                                row = next_symbol - 1
                                column = top_symbol - 1
                                relation = relation_matrix[row][column]

                            lost_handle.append(parse_stack.pop(len(parse_stack) - 1))
                            print "Reducibility error found."
                            print "The following statement will be discarded: ", lost_handle
                            print "The parse stack will be reset back to the last known good configuration.\n"
                            for i in range(len(lost_handle)):
                                semantic_stack.pop(len(semantic_stack) - 1)
                            match = True

                        ## This section performs a reduction if one is possible.
                        if potential_match == handle:
                            left_hand_side_symbol = reverse_variable_dictionary[left_hand_side]
                            reductions.append(production_number)
                            handle_symbols = []
                            pre_reduction_stack = []

                            for i in range(len(parse_stack)- 1):
                                pre_reduction_stack.append(parse_stack[i + 1])

                            for i in range(handle_length):
                                handle_symbols.append(reverse_variable_dictionary[potential_match.pop(0)])
                                parse_stack.pop(len(parse_stack) - 1)

                            ## This section checks for stackability errors and handles them if necessary.
                            if parse_stack[len(parse_stack) - 1] != '$':
                                parse_symbol = variable_dictionary[parse_stack[len(parse_stack) - 1]]

                            row = parse_symbol - 1
                            column = left_hand_side - 1
                            relation = relation_matrix[row][column]
                            if relation == '2':
                                lost_handle = []
                                lost_handle.append(parse_stack.pop(len(parse_stack) - 1))
                                top_symbol = variable_dictionary[parse_stack[len(parse_stack) - 1]]
                                next_symbol = variable_dictionary[parse_stack[len(parse_stack) - 2]]
                                row = next_symbol - 1
                                column = top_symbol - 1
                                relation = relation_matrix[row][column]
                                while relation != '3':
                                    lost_handle.append(parse_stack.pop(len(parse_stack) - 1))
                                    top_symbol = variable_dictionary[parse_stack[len(parse_stack) - 1]]
                                    next_symbol = variable_dictionary[parse_stack[len(parse_stack) - 2]]
                                    row = next_symbol - 1
                                    column = top_symbol - 1
                                    relation = relation_matrix[row][column]

                                lost_handle.append(parse_stack.pop(len(parse_stack) - 1))
                                print "Stackability error found!"
                                print "The following statement will be discarded: ", lost_handle
                                print "The parse stack will be reset back to the last known good configuration.\n"
                                for i in range(len(lost_handle)):
                                    semantic_stack.pop(len(semantic_stack) - 1)
                                match = True
                                
                            ## This section handles most of the parser flags
                            if relation != '2':
                                parse_stack.append(reverse_variable_dictionary[left_hand_side])
                                post_reduction_stack = []
                                
                                ## Semantic Analysis
                                semantic_output = SemanticAnalyzer.analyze(semantic_stack, variable_symbol_table, procedure_symbol_table, production_number, handle_length, inside_procedure, flags_dictionary, intermediate_code, declared_variable_list, local_declared_variable_list, label_list)
                                if semantic_output != None:

                                    if semantic_output[0] != None:    
                                        semantic_stack = []
                                        semantic_stack.extend(semantic_output[0])

                                    if semantic_output[1] != None:
                                        variable_symbol_table = copy.copy(semantic_output[1])

                                    if semantic_output[2] != None:
                                        procedure_symbol_table = copy.copy(semantic_output[2])

                                    if semantic_output[3] != None:
                                        inside_procedure = semantic_output[3]
        
                                    if semantic_output[4] != None:    
                                        intermediate_code = []
                                        intermediate_code.extend(semantic_output[4])
                                        
                                    if semantic_output[5] != None:    
                                        declared_variable_list = []
                                        declared_variable_list.extend(semantic_output[5])
                                        
                                    if semantic_output[6] != None:    
                                        local_declared_variable_list = []
                                        local_declared_variable_list.extend(semantic_output[6])

                                    if semantic_output[7] != None:
                                        label_list = []
                                        label_list.extend(semantic_output[7])
                                        
                                if len(parse_stack) != len(semantic_stack):
                                    size = len(semantic_stack) - len(parse_stack)

                                    for i in range(size):
                                        semantic_stack.pop(len(semantic_stack) - 1)

                                if flags_dictionary["12"]:
                                    print "\nThis is the Semantic Stack After Reduction: ", semantic_stack     

                                for i in range(len(parse_stack) - 1):
                                    post_reduction_stack.append(parse_stack[i + 1])

                                if flags_dictionary["10"]:
                                    parser_handle = ''

                                    for i in range(len(handle_symbols)):
                                        parser_handle = parser_handle + handle_symbols[i] + " "

                                    print "The matched handle is: ", parser_handle, "\n"

                                if flags_dictionary["7"]:
                                    parser_handle = ''

                                    for i in range(len(handle_symbols)):
                                        parser_handle = parser_handle + handle_symbols[i] + " "

                                    print "Reduction Made: ", parser_handle, "---->", left_hand_side_symbol, "\n"

                                if flags_dictionary["8"]:
                                    print "Stack Before Reduction: ", pre_reduction_stack
                                    print "Stack After Reduction: ", post_reduction_stack, "\n"

                                ## This section checks to make sure the parse stack doesn't need
                                ## to be reduced again after the previous reduction was made before
                                ## the next input symbol is pushed onto the parse stack
                                if parse_stack[len(parse_stack) - 1] != '$':
                                    parse_symbol = variable_dictionary[parse_stack[len(parse_stack) - 1]]

                                row = parse_symbol - 1
                                column = input_symbol - 1
                                relation = relation_matrix[row][column]

                                if relation != '2':
                                        match = True

                                if relation == '2':
                                    handle_length = len(parse_stack) - 1
                                    handle = []
                                    for i in range(handle_length):
                                        handle.append(variable_dictionary[parse_stack[i + 1]])

                if match != True:
                    if handle != []:
                        handle_length = handle_length - 1
                        handle.pop(0)
                    else:
                        match = True

                if match == True:
                    parse_stack.append(reverse_variable_dictionary[input_symbol])
                    semantic_stack.append(semantic_symbol_list.pop(0))
                    return parse_stack, character_pair_error, reductions, variable_symbol_table, semantic_stack, procedure_symbol_table, inside_procedure, intermediate_code, declared_variable_list, local_declared_variable_list, label_list

if __name__ == parse:
    parse()

