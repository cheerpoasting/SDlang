#########################################################################
#                                                                       #
#      Self-Documenting Programming Language with a focus on Business   #
#                                                                       #
# Version Number : 00.00.02-alpha-4                                     #
#                                                                       #
# Last Updated : 08 AUG 2025                                            #
#                                                                       #
# Program Purpose : This program will open a source file, and write its #
#   contents directly to an output file, without transforming it in     #
#   any way.                                                            #
#                                                                       #
# ACW : Began to create lexer. Can handle: white space, numbers,        #
#   letters, and handle unknown tokens gracefully.                      #
#                                                                       #
#########################################################################

# COMMON FILE ERROR TYPES
#Filenotfounderror
#PermissionError
#IsADirectoryError
#OSError/IOError
#UnicodeDecodeError
#Empty File

# IMPORT AREA

import sys
import os
from datetime import datetime
from Error_Handling import *

# UTILITY AREA.

def get_timestamp(format_type):
    now = datetime.now()

    if format_type == "date":
        return now.strftime("%Y-%m-%d")
    elif format_type == "time":
        return now.strftime("%H:%M")
    elif format_type == 'casual':
        return now.strftime("%d %b %Y, %I:%M %p")
    else:
        return now.strftime("%Y-%m-%d %H:%M:%S")  # Default to full

# TOKENIZING AREA.

class Token: # This will allow you to "create tokens", which have 4 peices of info
    def __init__(self, token_type, what_the_token_is, line_of_token, column_of_token):
        self.token_type = token_type
        self.actual_text = what_the_token_is
        self.line_number = line_of_token
        self.column_number = column_of_token

SDLang_keywords = {
    "ADDED": "KEYWORD_OPERATOR",
    "TO": "KEYWORD_CONTEXTUAL"
}

# PARSING AREA.

#def visualize_parsing():
    

# CODE AREA.

def read_source_file(source_path):
    if not os.path.exists(source_path): #check to see if the file exists
        SDLangErrors.handle_file_not_found(source_path, "transpile our program")

    allowed_extensions = ['.sdl', '.sdlang', '.txt']
    file_extension = os.path.splitext(source_path)[1].lower()
    if file_extension not in allowed_extensions:
        SDLangErrors.handle_invalid_file_type(source_path, "transpile our program", file_extension)
    
    if os.path.getsize(source_path) == 0: #check if file is empty
        SDLangErrors.handle_empty_file(source_path, "transpile our program")
    try:
        with open(source_path, 'r', encoding='utf-8') as source_file:
            source_content = source_file.read()
            return source_content
    except UnicodeDecodeError:
        error_code = SDLangErrors.INVALID_ENCODING
        SDLangErrors.handle_invalid_encoding(source_path, "transpile our program")
    except:
        error_code = SDLangErrors.READ_FAILED
        print(f"Read Error - {source_path} : {error_code}")
        sys.exit(SDLangErrors.READ_FAILED)
        
def tokenize(thing_to_be_lexed):
    list_of_tokens = [] #create an empty list that the tokens will go in

    position = 0
    line_number = 1
    column_number = 1

    while position < len(thing_to_be_lexed): #when we haven't hit the end of the file
        current_character = thing_to_be_lexed[position]

        # Handle whitespace !!! "" is empty string, " " is space
        if current_character == " " or current_character =="\t": # if the character is space or tab
            column_number = column_number + 1 #just move to the next character
            position = position + 1 #tell the program we moved to the next character
            continue

        # Handle newline
        if current_character == "\n":
            line_number = line_number + 1 #increment to next line
            column_number = 1 #reset to first column of line
            position = position + 1 # tell the program we moved to the next character
            continue

        else:
            text = ""
            start_line = line_number
            start_column = column_number
            token_type = "UNCLASSIFIED"

            while position <len(thing_to_be_lexed) and not thing_to_be_lexed[position].isspace():
                if thing_to_be_lexed[position].isalpha():
                    text = text + thing_to_be_lexed[position].upper()
                else:
                    text = text + thing_to_be_lexed[position]
                position = position + 1
                column_number = column_number + 1

            new_token = Token(token_type, text, start_line, start_column)
            list_of_tokens.append(new_token)
            continue

    return list_of_tokens

def classify_tokens(tokens_to_be_classified):

    for token in tokens_to_be_classified:
        if token.actual_text.isalpha():
            if token.actual_text in SDLang_keywords:
                token.token_type = SDLang_keywords[token.actual_text]
            else:
                token.token_type = "WORD"
        elif token.actual_text.isdigit():
            token.token_type = "NUMBER"
        else:
            token.token_type = "UNKNOWN"
    
    return tokens_to_be_classified


def save_tokens_readable(tokens, filename):
    try:
        with open(filename, 'w', encoding='utf-8') as lex_file:
            for token in tokens:
                lex_file.write(f"({token.token_type}, \"{token.actual_text}\", Line {token.line_number}, Column {token.column_number})\n")
            print(f"successfully wrote to {filename}")
    except:
        error_code = SDLangErrors.WRITE_FAILED
        print(f"Write Error - {filename} : {error_code}")
        sys.exit(error_code)


def transform_content(thing_to_be_transformed):
    print("contents would be transformed here in the future")
    return thing_to_be_transformed

##so maybe it will go token by token, and each token can become a node,
##if there is no other rule associated associated with it.
##then, when I hit a keyword, I then look for its arguments, and
##in this case "to" is an argument of "added"?
##
##so, maybe I will first want to create a visual way of representing
##the "level" of tokens, so that I can confirm if they are being
##manipulated correctly?



def write_output_file(content_to_save, output_path):
    try:
        with open(output_path, 'w', encoding='utf-8') as output_file:
            output_file.write(content_to_save)
            print(f"successfully wrote {len(content_to_save)} characters to {output_path}")
    except:
        print("Normal write failed, attempting to write tokens...")
        try:
            token_content = ""
            for token in content_to_save:
                token_content = token_content + f"{token.token_type},{token.actual_text},{token.line_number},{token.column_number}\n"
        
            # Try to write the tokens
            with open(output_path, 'w', encoding='utf-8') as output_file:
                output_file.write(token_content)
                print(f"successfully wrote {len(token_content)} characters of token data to {output_path}")
        except:
            error_code = SDLangErrors.WRITE_FAILED
            print(f"Write Error - {output_path} : {error_code}")
            sys.exit(error_code)

def main():
    print(f"[{get_timestamp('casual')}] Program \"Main_Controller\" began running.\n")
    source_content = read_source_file("file-to-be-parsed.sdlang")
    lexed_content = tokenize(source_content)
    classified_content = classify_tokens(lexed_content)
    save_tokens_readable(classified_content, "lexer_tokens.txt")
    transformed_content = transform_content(lexed_content)
    write_output_file(transformed_content, "final-python-file.py")
    print(f"\n[{get_timestamp('casual')}] Program \"Main_Controller\" finished running.")

if __name__ == "__main__":
    main()
