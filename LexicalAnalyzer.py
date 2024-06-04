## Sean Bloomsburg
## sbloomsburg@gmail.com
##
## This module breaks the source code down
## into component tokens. The tokens are comprised
## of a syntactical unit and a code that can be
## identified by the parser.
##

import re
import string


def analyze(code_string, comment_end):

    ## List of reserve words
    reserve_words = ["END","PROGRAM","DECLARE","REAL","INTEGER","PROCEDURE",
                             "VALUE", "REFERENCE","MAIN","INPUT","OUTPUT","CALL",
                             "ELSE","IF","THEN", "INCREMENT","BY","FOR","UNTIL","DO"]

    ## The regular expressions used to analyze the input string
    white_space_re = re.compile('[ \t\n]')
    comment_type1_start_re = re.compile('/\*')
    comment_type1_end_re = re.compile('\*/')
    comment_type2_start_re = re.compile('//')
    comment_type2_end_re = re.compile('[\n]')
    flag_start_re = re.compile('##[\+|\-\d+]*')
    flag_end_re = re.compile('##')
    real_number_re = re.compile('([+]|[-])*\d+[.]\d+')
    integer_re = re.compile('([+]|[-])*\d+')
    reserve_word_re = re.compile('[A-Z]+')
    identifier_re = re.compile('[a-z]+([a-z]|[0-9]|\-|_)*')
    operator_re = re.compile(';|\-|,|\[|\]|\(|\)|:|!|<|>|\+|\*|/|{|}|=')
    double_operator_re = re.compile('(==)|(!=)|(<=)|(>=)|(<-)|(::)|(\|\|)|(&&)')
    invalid_operator_re = re.compile('`|~|@|\$|\^|_|\.|\'|"|\?|%|\\\\')

    ## Initializes primary variables to be returned
    input_string = code_string
    no_output = ''
    error = ''

    if input_string == '':
        return no_output, input_string, comment_end, error

    ## Handles comments
    while comment_type1_start_re.match(input_string) or comment_end == False:
        comment_end = False

        while comment_end == False:
            if comment_type1_end_re.search(input_string):
                comment_end = comment_type1_end_re.search(input_string).span()
                input_string = input_string[comment_end[1]:]
                comment_end = True
                return no_output, input_string, comment_end, error

            else:
                input_string = ''
                return no_output, input_string, comment_end, error

    while comment_type2_start_re.match(input_string):
        start = comment_type2_start_re.search(input_string).span()
        comment_end = comment_type2_end_re.search(input_string).span()
        input_string = input_string[comment_end[1]:]
        if input_string == '':
            return no_output, input_string, True, error

    ## Handles white space
    while white_space_re.match(input_string):
        length = white_space_re.match(input_string).span()
        input_string = input_string[length[1]:]
        if input_string == '':
            return no_output, input_string, True, error
    
    ## Also handles comments
    while comment_type1_start_re.match(input_string) or comment_end == False:
        comment_end = False

        while comment_end == False:

            if comment_type1_end_re.search(input_string):
                comment_end = comment_type1_end_re.search(input_string).span()
                input_string = input_string[comment_end[1]:]
                comment_end = True
                return no_output, input_string, comment_end, error

            else:
                input_string = ''
                return no_output, input_string, comment_end, error

    while comment_type2_start_re.match(input_string):
        start = comment_type2_start_re.search(input_string).span()
        comment_end = comment_type2_end_re.search(input_string).span()
        input_string = input_string[comment_end[1]:]
        if input_string == '':
            return no_output, input_string, True, error

    ## Handles flags
    while flag_start_re.match(input_string):
        flags = flag_start_re.search(input_string).group()
        start = flag_start_re.search(input_string).span()
        input_string = input_string[:start[0]] + input_string[start[1]:]
        tag = "001"
        token = (tag, flags)
        if input_string != '':
            comment_end = flag_end_re.search(input_string).span()
            input_string = input_string[comment_end[1]:]
        return token, input_string, True, error

    ## Handles reserve words
    reserve_word = ''
    while reserve_word_re.match(input_string):
        reserve_word = reserve_word_re.search(input_string).group()
        length = reserve_word_re.search(input_string).span()
        input_string = input_string[length[1]:]
        tag = "002"
        token = (tag, reserve_word)
        if reserve_word in reserve_words:
            return token, input_string, True, error

        else:
            error = "is an invalid Reserve Word."
            tag = "error"
            token = (tag, reserve_word)
            return token, input_string, True, error

    ## Handles real numbers
    input_number = ''
    output_number = ''
    temp = []
    sign = ''
    while real_number_re.match(input_string):
        input_number = real_number_re.search(input_string).group()
        length = real_number_re.search(input_string).span()
        input_string = input_string[length[1]:]
        tag = "003"
        size = len(input_number)
        for i in range(size):
            temp.append(input_number[i])
        if temp[0] == "-":
            sign = temp.pop(0)
        if temp[0] == "+":
            sign = temp.pop(0)
        if len(temp) > 1:
            while temp[0] == '0':
                temp.pop(0)
        for i in range(len(temp)):
            output_number = output_number + str(temp[i])
        if len(output_number) > 7:
            error = "is an invalid Real Number.\n\t Outside range."
            tag = "error"
        input_number = sign + output_number
        input_number = float(input_number)
        token = (tag, input_number)
        return token, input_string, True, error

    ## Handles integers
    input_number = ''
    output_number = ''
    temp = []
    sign = ''
    count = 0
    while integer_re.match(input_string):
        input_number = integer_re.search(input_string).group()
        length = integer_re.search(input_string).span()
        input_string = input_string[length[1]:]
        tag = "004"
        size = len(input_number)
        for i in range(size):
            temp.append(input_number[i])
        if temp[0] == "-":
            sign = temp.pop(0)
        if temp[0] == "+":
            sign = temp.pop(0)
        if len(temp) > 1:
            while temp[0] == '0':
                temp.pop(0)
        if len(temp) > 1:
            while temp[len(temp)-1] == '0':
                temp.pop(len(temp)-1)
                count = count + 1   
        for i in range(len(temp)):
            output_number = output_number + str(temp[i]) 
        if len(output_number) > 9:
            error = "is an invalid Integer.\n\t Outside range."
            tag = "error"
        input_number = sign + output_number
        input_number = int(input_number) * 10 ** count
        token = (tag, input_number)
        return token, input_string, True, error

    ## Handles identifiers
    word = ''
    while identifier_re.match(input_string):
        word = identifier_re.search(input_string).group()
        length = identifier_re.search(input_string).span()
        input_string = input_string[length[1]:]
        if len(word) > 16:
            original_identifier = word
            error = "was an invalid Identifier.\n\t Excess characters removed.\n\t Changed from " + original_identifier
            word = word[0:16]
        tag = "005"
        token = (tag, word)
        return token, input_string, True, error

    ## Handles double ASCII characters
    operator = ''
    while double_operator_re.match(input_string):
        operator = double_operator_re.search(input_string).group()
        length = double_operator_re.search(input_string).span()
        input_string = input_string[length[1]:]
        tag = "006"
        token = (tag, operator)
        return token, input_string, True, error

    ## Handles ASCII characters
    operator = ''
    while operator_re.match(input_string):
        operator = operator_re.search(input_string).group()
        length = operator_re.search(input_string).span()
        input_string = input_string[length[1]:]
        tag = "007"
        token = (tag, operator)
        return token, input_string, True, error

    ## Handles invalid ASCII characters
    operator = ''
    while invalid_operator_re.match(input_string):
        operator = invalid_operator_re.search(input_string).group()
        length = invalid_operator_re.search(input_string).span()
        input_string = input_string[length[1]:]
        error = "is an invalid operator."
        token = ("008", operator)
        return token, input_string, True, error

    if input_string == '':
        return no_output, input_string, True, error

if __name__ == analyze:
    analyze()
