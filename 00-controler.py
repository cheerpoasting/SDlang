#########################################################################
#                                                                       #
#      Self-Documenting Programming Language with a focus on Business   #
#                                                                       #
# Version Number : 00.00.01-alpha-1                                     #
#                                                                       #
# Last Updated : 08 AUG 2025                                            #
#                                                                       #
# Program Purpose : This program will open a source file, and write its #
#   contents directly to an output file, without transforming it in     #
#   any way.                                                            #
#                                                                       #
# ACW : Began to implement error message templates in the               #
#   class SDLangErrors. To see an example look at                       #
#   def handle_file_not_found, the read_source_file FileNotFound.       #
#                                                                       #
#########################################################################

# TEMPLATE
# Open input file
# Transform contents (later)
# Write Contents to output file

#

# COMMON FILE ERROR TYPES
#Filenotfounderror
#PermissionError
#IsADirectoryError
#OSError/IOError
#UnicodeDecodeError
#Empty File

# IMPORT AREA

import sys
from datetime import datetime

# DATA STRUCTURE AREA.

class SDLangErrors: #mixing variables and classes works correctly
    
    INVALID_ENCODING = "SDL-E001"
    EMPTY_FILE = "SDL-E002"
    
    READ_FAILED = "SDL-E400" #generic read

    PERMISSION_DENIED = "SDL-E403"
    
    FILE_NOT_FOUND = "SDL-E404"

    @staticmethod #allow you to call the function without making an object
    def handle_file_not_found(file_path):
        error_code = SDLangErrors.FILE_NOT_FOUND
        print(f"I couldn't find your file \"{file_path}\" : {error_code}")
        sys.exit(error_code)
    
    
    WRITE_FAILED = "SDL-E500" #generic write

#Source Variables.
# source_path: str #the file path for the source file
# source_file #textIO, the actual source file
# source_content: str #the textual contents of the file

#Transformation Variables.
# transformed_content: str
# thing_to_be_transformed: str

#Output Variables.
# output_path: str #the file path for the output file
# output_file #textIO, the actual output file
# output_content: str # the textual contents of the output file

# CODE AREA.

def read_source_file(source_path):
    try:
        with open(source_path, 'r', encoding='utf-8') as source_file:
            source_content = source_file.read()
            print(f"successfully read {len(source_content)} characters from {source_path}")
            return source_content
    except FileNotFoundError:
        print(f"I didn't transpile your program because")
        SDLangErrors.handle_file_not_found(source_path)
    except:
        error_code = SDLangErrors.READ_FAILED
        print(f"Read Error - {source_path} : {error_code}")
        sys.exit(SDLangErrors.READ_FAILED)

def transform_content(thing_to_be_transformed):
    print("contents would be transformed here in the future")
    return thing_to_be_transformed

def write_output_file(content_to_save, output_path):
    try:
        with open(output_path, 'w', encoding='utf-8') as output_file:
            output_file.write(content_to_save)
            print(f"successfully wrote {len(content_to_save)} characters to {output_path}")
    except:
        error_code = SDLangErrors.WRITE_FAILED
        print(f"Write Error - {output_path} : {error_code}")
        sys.exit(error_code)

def main():
    print("Program \"00-controller\" began running.")
    source_content = read_source_file("file-tobe-parsed.sdlang")
    transformed_content = transform_content(source_content)
    write_output_file(transformed_content, "final-python-file.py")

if __name__ == "__main__":
    main()
