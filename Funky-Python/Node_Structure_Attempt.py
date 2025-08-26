# Imports. 
from Node_Token_Stuff import *
from Lookups import *

# Open/Read Files. 
def open_file(file_name):

    with open(file_name, 'r') as file:
        contents = file.read()

    return contents

# Main Program.

def main():

    raw_file = open_file("basic-verbose-python.txt")
    lexed_tokens = Lexer(raw_file).lex()
    print(lexed_tokens)

if __name__ == "__main__":
    main()
