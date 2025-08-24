import sys
from Create_Tokens import *

def merge_tokens_first_pass(tokens):

    token_stream = []

    position = 0

    while position < len(tokens):

        current = tokens[position]

        if (current.actual_text == "OVERVIEW" and
            current.consumed == False):
            if position + 1 < len(tokens):
                new_token = Token(current.actual_text,
                    current.line, current.column,
                    current.token_type, current.subtype, True)
                position = position + 2
                token_stream.append(new_token)
            else:
                sys.exit(f"Invalid Syntax. \"Overview\" requires a period, none found. L{current.line}C{current.column}")
            continue


        if (current.actual_text == "WENT" and
            current.consumed == False):
            
            peek = position + 1
            
            if (peek < len(tokens) and
                tokens[peek].actual_text == "TO"):
                new_token = Token(current.actual_text,
                    current.line, current.column,
                    current.token_type, current.subtype, True)
                position = position + 2
                token_stream.append(new_token)
            else:
                sys.exit(f"Invalid Syntax. L{current.line}C{current.column}")
            continue

        if current.token_type == "WORD":

            peek = position + 1

            if(peek < len(tokens) and
                tokens[peek].actual_text == "PARAGRAPH"):
                new_token = Token(current.actual_text,
                    current.line, current.column,
                    "FUNCTION", "PARAGRAPH")
                position = position + 2
                token_stream.append(new_token)
                continue
                
        else:
            token_stream.append(current)
            position = position + 1

    return token_stream

def merge_tokens_second_pass(tokens):

    token_stream = []

    position = 0

    while position < len(tokens):

        current = tokens[position]

        if (current.actual_text == "WENT" and
            current.consumed == True):
            peek = position + 1
            if (peek < len(tokens) and
                tokens[peek].subtype == "PARAGRAPH" and
                tokens[peek].actual_text != "PARAGRAPH"):
                peek_token = tokens[peek]
                new_token = Token(peek_token.actual_text,
                    current.line, current.column,
                    current.token_type, current.subtype, False)
                token_stream.append(new_token)
                position = position + 2
                continue
            
        if (current.subtype == "PARAGRAPH" and
            current.actual_text != "PARAGRAPH" and
            current.consumed == False):
            peek = position + 1
            
            if (peek < len(tokens) and
                tokens[peek].actual_text == "."):
                peek_token = tokens[peek]
                new_token = Token(current.actual_text,
                    current.line, current.column,
                    current.token_type, "DEFINITION", True)
                token_stream.append(new_token)
                position = position + 2
                continue
            

        if (current.actual_text == "TODO" and
            current.consumed == False):
            peek = position + 1
            if (peek < len(tokens) and
                tokens[peek].actual_text == "."):
                token = current
                new_token = Token(token.actual_text,
                    token.line, token.column,
                    token.token_type, token.subtype, True)
                position = position + 2
                token_stream.append(new_token)
                continue

        if (current.actual_text == "."):
            position = position + 1
            continue

        else:
            token_stream.append(current)
            position = position + 1

    return token_stream

def merge_tokens(tokens):
    first_merge = merge_tokens_first_pass(tokens)
    return merge_tokens_second_pass(first_merge)
