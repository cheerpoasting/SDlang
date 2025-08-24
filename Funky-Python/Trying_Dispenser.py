from Dispenser import *
from Create_Tokens import *
from Merge_Tokens import *
import sys

def read_file(file_name):
    try:
        with open(file_name, 'r') as file:
            contents = file.read()
        return contents
    except:
        print(f"couldn't read file")

def write_useable_python(content_to_save, file_name):
    with open(file_name, 'w') as file:
        file.write(content_to_save)

def pythonify(name):
    new_name = name.lower().replace("-","_")
    return new_name

def indent_functions(tokens):

    list_of_split_functions = []
    main = []

    position = 0
    indentation = 0

    put_in_main = False

    while position < len(tokens):
        token = tokens[position]

        if token.subtype == "CALL":

            actual_text = pythonify(token.actual_text)

            text = f"{actual_text}()\n"
            
            new_token = Token(token.actual_text, token.line,
                token.column,token.token_type, token.subtype,
                token.consumed, indentation, text)

            if put_in_main == True:
                main.append(new_token)
            else: 
                list_of_split_functions.append(new_token)

            position = position + 1
            continue

        if token.subtype == "PASS":

            text = pythonify(token.subtype)

            new_token = Token(token.actual_text, token.line,
                token.column,token.token_type, token.subtype,
                token.consumed, indentation, text)
            
            if put_in_main == True:
                main.append(new_token)
            else: 
                list_of_split_functions.append(new_token)

            position = position + 1
            continue
        
        if token.subtype == "MAIN":
            
            indentation = 0
            text = "\ndef main():\n"
            
            new_token = Token(token.actual_text, token.line,
                token.column,token.token_type, token.subtype,
                token.consumed, indentation, text)

            indentation = indentation + 1

            put_in_main = True
            
            if put_in_main == True:
                main.append(new_token)
            else: 
                list_of_split_functions.append(new_token)

            position = position + 1
            continue

        if token.subtype == "DEFINITION":

            actual_text = pythonify(token.actual_text)
            
            indentation = 0
            put_in_main = False
            
            text = f"\ndef {actual_text}():\n"
            
            new_token = Token(token.actual_text, token.line,
                token.column,token.token_type, token.subtype,
                token.consumed, indentation, text)

            indentation = indentation + 1
            
            if put_in_main == True:
                main.append(new_token)
            else: 
                list_of_split_functions.append(new_token)

            position = position + 1
            
            continue

        else:
            sys.exit()

    for token in main:
        list_of_split_functions.append(token)

    return list_of_split_functions
        
    

def main():
    raw_python = read_file("basic-verbose-python.txt")
    #print(raw_python)

    tokenized_python = tokenize(raw_python)
    #print(tokenized_python)

    merged_python = merge_tokens (tokenized_python)
    #print(merged_python)

    formatted_python = indent_functions(merged_python)
    print(formatted_python)

    joined_python = " ".join(token.print_text for token in formatted_python)
    joined2_python = joined_python + "\nif __name__ == \"__main__\":\n    main()"
    print(joined2_python)
    write_useable_python(joined2_python, "converted-to-python.py")

if __name__ == "__main__":
    main()

