## Sean Bloomsburg
## sbloomsburg@gmail.com
##
## This compiler uses a Simple Precedence Grammar
## The grammar file stores the variables, production
## rules, and the grammar relation matrix. This module
## extracts those elements into useful data structures.
##

import string
import re


def analyze():
    integer_re = re.compile('\d+')
    white_space_re = re.compile('[ \t\n]')
    grammar = open( "spgrammar.txt", "r")

    variable_dictionary = {}
    variable = ''
    productions = []
    relation_matrix = []
    line_number = 1

    for line in grammar:
        current_line = line
        temp = []

        ## Puts all the terminal and nonterminal variables into list
        if line_number < 89:
            variable = line.strip()
            variable_dictionary[variable] = line_number

        ## Puts all grammar production rules into an easy access matrix
        if line_number > 88:
            if line_number < 194:
                current_line = line
                number = ''

                while integer_re.search(current_line):
                    number = integer_re.search(current_line).group()
                    length = integer_re.search(current_line).span()
                    current_line = current_line[length[1]:]
                    temp.append(number)

            if temp != []:
                productions.append(temp)
                
        ## Puts the grammar relation matrix into...another matrix!
        if line_number > 193:
            current_line = line
            number = ''

            while integer_re.search(current_line):
                number = integer_re.search(current_line).group()
                length = integer_re.search(current_line).span()
                current_line = current_line[length[1]:]

            for i in range(len(number)):
                temp.append(number[i])

            relation_matrix.append(temp)
        line_number +=1

    return variable_dictionary, productions, relation_matrix

if __name__ == analyze:
    analyze
