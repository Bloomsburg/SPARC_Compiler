## Sean Bloomsburg
## sbloomsburg@gmail.com
##
## This is a basic compiler that compiles a C-like language
## to assembly code for a Sun SPARC processor. 
##

import CodeGenerator
import LexicalAnalyzer
import Parser
import SemanticAnalyzer
import datetime
import copy
import re


def main():
    ## Get's the current date and time
    current = datetime.datetime.now()

    ## Prints a header to the output
    print "##Name: SEAN BLOOMSBURG"
    print "##Email Address: sbloomsburg@gmail.com"       
    print "##Current Date and Time:", str(current)

    ## Reads the source file of code to be compiles
    test_data = open( "bubblesort.txt", "r")

    ## Primary Variables
    flag_check_re = re.compile('([+]|[-])*\d+')
    flags_dictionary = {}

    for i in range(33):
        flags_dictionary[str(i)] = False
    flags_dictionary["1"] = True
    flags_dictionary["13"] = True

    comment_end = True
    lexical_analysis = []
    valid_tag = ["005", "004", "006","007", "002"]
    reserved_tags = ["002", "006", "007"]

    parse_stack = []
    parse_stack.append('$')

    semantic_stack = []
    semantic_stack.append('$')
    reductions = []
    variable_symbol_table = {}
    procedure_symbol_table = {}
    inside_procedure = False
    character_pair_error = False
    declared_variable_list = []
    local_declared_variable_list = []
    intermediate_code = []
    label_list = []

    ## Reads each line of source as more tokens are required by the parser
    for line in test_data:
        code_string = line
        end_of_code = False
        flags_to_set = []
        print "\nThe current line to be analyzed: \n"
        print line

        while end_of_code == False:

            ## Lexical analyzer returns output to list: lexical_analysis
            lexical_analysis.append( LexicalAnalyzer.analyze(code_string, comment_end) ) 

            ## Puts output into tuple to be broken up
            lexical_output = lexical_analysis.pop(0)
            
            ## The token, remainder of the string of source code,
            ## if working through a multi-line comment, whether or not the
            ## end of the comment had been found, and an error if any is found.
            token = lexical_output[0]
            code_string = lexical_output[1]
            comment_end = lexical_output[2]
            error = lexical_output[3]

            ## Sets or unsets flags
            ## flags_dictionary are special tokens that alter the compiler output
            if type(token) == tuple:
                if token[0] == "001":
                    flag_string = str(token[1])

                    while flag_check_re.search(flag_string):
                        flag = flag_check_re.search(flag_string).group()
                        length = len(flag)
                        flag_string = flag_string[length:]
                        if '+' in flag:
                            flag = flag[1:]
                            flags_dictionary[flag] = True
                            if flags_dictionary["0"]:
                                for i in range(len(flags_dictionary)):
                                    flags_dictionary[str(i)] = True
                        if '-' in flag:
                            flag = flag[1:]
                            flags_dictionary[flag] = False
                            if flags_dictionary["0"]:
                                for i in range(len(flags_dictionary)):
                                    flags_dictionary[str(i)] = False
                            flags_dictionary["1"] = True           

            ## Prints error statement if any
            if error != "":
                print "Error: ", token[1], error

            if flags_dictionary["20"]:
                if ("20", "Flag", "-" , "-") not in intermediate_code:
                    intermediate_code.append(("20", "Flag", "-" , "-"))

            ## Checks to see if a valid token has been found to be sent to the parser
            key = 0 
            if type(token) == tuple:
                if token[0] in valid_tag:
                    if flags_dictionary["2"]:
                        print "Valid Token: ", token
                    if token[0] in reserved_tags:
                        token = (token[1], token[1])
                    if token[0] == "005":
                        token = ("var", token[1])
                    if token[0] == "004":
                        token = ("integer", token[1])
                    if token[0] == "003":
                        token = ("real", token[1])

                    ## This is where the parsing magic happens
                    parser_output = Parser.parse( token, 
                                                             parse_stack, 
                                                             flags_dictionary, 
                                                             character_pair_error,
                                                             reductions,
                                                             variable_symbol_table,
                                                             semantic_stack,
                                                             procedure_symbol_table,
                                                             inside_procedure,
                                                             intermediate_code,
                                                             declared_variable_list,
                                                             local_declared_variable_list,
                                                             label_list)

                    if parser_output != None:

                        if parser_output[0] != None:    
                            parse_stack = []
                            parse_stack.extend(parser_output[0])

                        if parser_output[1] != None:
                            character_pair_error = parser_output[1]

                        if parser_output[2] != None:
                            reductions = []
                            reductions.extend(parser_output[2])

                        if parser_output[3] != None:
                            variable_symbol_table = copy.copy(parser_output[3])

                        if parser_output[4] != None:
                            semantic_stack = []
                            semantic_stack.extend(parser_output[4])

                        if parser_output[5] != None:
                            procedure_symbol_table = copy.copy(parser_output[5])

                        if parser_output[6] != None:
                            inside_procedure = parser_output[6]

                        if parser_output[7] != None:
                            intermediate_code = []
                            intermediate_code.extend(parser_output[7])
                            
                        if parser_output[8] != None:
                            declared_variable_list = []
                            declared_variable_list.extend(parser_output[8])
                            
                        if parser_output[9] != None:
                            local_declared_variable_list = []
                            local_declared_variable_list.extend(parser_output[9])

                        if parser_output[10] != None:
                            label_list = []
                            label_list.extend(parser_output[10])
                            
            if comment_end == False:
                end_of_code = True

            if code_string == '':
                end_of_code = True

    ## Final parser reduction
    parser_output = Parser.parse( token,
                                              parse_stack,
                                              flags_dictionary,
                                              character_pair_error, 
                                              reductions,
                                              variable_symbol_table,
                                              semantic_stack,
                                              procedure_symbol_table,
                                              inside_procedure,
                                              intermediate_code, 
                                              declared_variable_list,
                                              local_declared_variable_list,
                                              label_list)

    if parser_output != None:

        if parser_output[0] != None:    
            parse_stack = []
            parse_stack.extend(parser_output[0])

        if parser_output[1] != None:
            character_pair_error = parser_output[1]

        if parser_output[2] != None:
            reductions = []
            reductions.extend(parser_output[2])

        if parser_output[3] != None:
            variable_symbol_table = copy.copy(parser_output[3])

        if parser_output[4] != None:
            semantic_stack = []
            semantic_stack.extend(parser_output[4])

        if parser_output[5] != None:
            procedure_symbol_table = copy.copy(parser_output[5])

        if parser_output[6] != None:
            inside_procedure = parser_output[6]

        if parser_output[7] != None:
            intermediate_code = []
            intermediate_code.extend(parser_output[7])
            
        if parser_output[8] != None:
            declared_variable_list = []
            declared_variable_list.extend(parser_output[8])
            
        if parser_output[9] != None:
            local_declared_variable_list = []
            local_declared_variable_list.extend(parser_output[9])

        if parser_output[10] != None:
            label_list = []
            label_list.extend(parser_output[10])

    if flags_dictionary["16"]:
        print "\nThe Final Variable Symbol Table: ", variable_symbol_table
    for i in range(len(intermediate_code)):
        print intermediate_code[i]

    assembly_code = CodeGenerator.generate(intermediate_code)
    print "\n\n\n"
    print "The assembly code generated: "

    output_file = open('bubblesort.s', 'w')
    for i in range(len(assembly_code)):
        print assembly_code[i]
        output_file.write(assembly_code[i] + "\n")
    output_file.close()

    ## Flag 1 allows the source code to be printed as part of the output
    if flags_dictionary["1"]:

        ## Prints the source code for ClearRegister.py
        clear_reg_source = open( "ClearRegister.py", "r")
        print "\n\n##The source code for ClearRegister.py:\n"
        for line in clear_reg_source:
            print line

        ## Prints the source code for CodeGenerator.py
        code_generator_source = open( "CodeGenerator.py", "r")
        print "\n\n##The source code for CodeGenerator.py:\n"
        for line in code_generator_source:
            print line

        ## Prints the source code for RegisterAllocation.py
        register_allocation_source = open( "RegisterAllocation.py", "r")
        print "\n\n##The source code for RegisterAllocation.py:\n"
        for line in register_allocation_source:
            print line            

        ## Prints the source code for LexicalAnalyzer.py
        lex_source = open( "LexicalAnalyzer.py", "r")
        print "\n\n##The source code for LexicalAnalyzer.py:\n"
        for line in lex_source:
            print line

        ## Prints the source code for GetType.py
        get_type_source = open( "GetType.py", "r")
        print "\n\n##The source code for Get_Type.py:\n"
        for line in get_type_source:
            print line

        ## Prints the source code for GrammarAnalyzer.py
        grammar_analysis_source = open( "Grammar_Analysis.py", "r")
        print "\n\n##The source code for Grammar_Analysis.py:\n"
        for line in grammar_analysis_source:
            print line

        ## Prints the source code for Parser.py
        Parser_Source = open( "Parser.py", "r")
        print "\n\n##The source code for Parser.py:\n"
        for line in Parser_Source:
            print line

        ## Prints the source code for SemanticAnalyzer.py
        Semantic_Source = open( "SemanticAnalyzer.py", "r")
        print "\n\n##The source code for Semantic_Analyzer.py:\n"
        for line in Semantic_Source:
            print line

        ## Prints the source code for compiler.py
        Main_Source = open( "Compiler.py", "r")
        print "\n\n##The source code for compiler.py:\n"
        for line in Main_Source:
            print line

main()

    
