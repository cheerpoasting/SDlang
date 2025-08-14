#########################################################################
#                                                                       #
#      Self-Documenting Programming Language with a focus on Business   #
#                                                                       #
# Version Number : 00.00.01-alpha-4                                     #
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
#   Additionally, began to do unit testing with Unit Test Controller.   #
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

def get_timestamp(format_type):
    now = datetime.now()

    if format_type == "date":
        return now.strftime("%Y-%m-%d")
    elif format_type == "time":
        return now.strftime("%H:%M")
    elif format_type == "casual":
        return now.strftime("%d %b %Y, %I:%M %p")
    else:
        return now.strftime("%Y-%m-%d %H:%M:%S")  # Default to full

# CODE AREA.

def read_source_file(source_path):
    if not os.path.exists(source_path): #check to see if the file exists
        print(f"I didn't transpile your program because")
        SDLangErrors.handle_file_not_found(source_path)
    try:
        with open(source_path, 'r', encoding='utf-8') as source_file:
            source_content = source_file.read()
            print(f"successfully read {len(source_content)} characters from {source_path}")
            return source_content
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
    print(f"[{get_timestamp("casual")}] Program \"Main_Controller\" began running.\n")
    source_content = read_source_file("file-to-be-parsed.sdlang")
    transformed_content = transform_content(source_content)
    write_output_file(transformed_content, "final-python-file.py")
    print(f"\n[{get_timestamp("casual")}] Program \"Main_Controller\" finished running.")

if __name__ == "__main__":
    main()
