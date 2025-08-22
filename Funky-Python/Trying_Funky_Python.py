class Token:
    def __init__ (self, token_type, actual_text, line_number, column_number, token_subtype=None, period_consumed=False):
        self.token_type = token_type
        self.token_subtype = token_subtype
        self.period_consumed = period_consumed
        self.actual_text = actual_text
        self.line_number = line_number
        self.column_number = column_number

    def __str__(self): # how it automatically represents itself as a string
        return f"{self.actual_text}"

    def __repr__(self): # how it appears in a list
        return f"\n{self.token_type}_{self.token_subtype}_{self.period_consumed}\t\t\t\tL{self.line_number}C{self.column_number}\n\t\t\"{self.actual_text}\" \t\t\t\t"

class TokenFormatter:
    def __init__ (self, actual_text, indentation):
        self._actual_text = actual_text
        self.indentation = indentation
        
    def __repr__(self):
        return f"{self.actual_text}"

    @property
    def actual_text(self):
        return "\t" * self.indentation + self._actual_text

def load_verbose_python(file_name):
    with open(file_name, 'r') as file:
        verbose_python = file.read()
        return verbose_python

def write_useable_python(content_to_save, file_name):
    with open(file_name, 'w') as file:
        file.write(content_to_save)


#Lookup Tables.

KEYWORD_LOOKUP_SUBTYPE = {
    "OVERVIEW": "MAIN",
    "TODO": "PASS",
    "PARAGRAPH": "FUNCTION"
}

KEYWORD_LOOKUP_ARGUMENTS = {
    "OVERVIEW": {
        "NUMBER": 1,
        "CALL": ""
    },
    "TODO": {
        "NUMBER": 1,
        "CONSUME PERIOD": True
    },
    "PARAGRAPH": {
        "NUMBER": 1,
        "CALL": ""
    }
}

SPECIAL_LOOKUP = {
    "@": {
        "token_type": "SYMBOL",
        "token_subtype": "AT-SIGN"
    },
    ".": {
        "token_type": "PUNCTUATION",
        "token_subtype": "PERIOD"
    }
}

#def translate(content_to_translate):
#tokenize
#classify
#parse

# "normalize" content at some point

def special_character(input_thing):
    if (not input_thing.isalnum() and
        input_thing != "-" and input_thing !="'"):
        #alnum checks for any mix of letters and numbers
        return True
    else:
        return False

def tokenize(thing_to_tokenize):
    list_of_tokens = []

    position = 0
    line = 1
    column = 1

    while position < len(thing_to_tokenize):
        current_character = thing_to_tokenize[position]

        # Ignore These Characters

        if current_character == " " or current_character =="\t":
            # space or tab character
            position = position + 1
            column = column + 1
            continue

        # Reset Line on these characters

        if current_character == "\n":
            #newline character
            position = position + 1
            line = line + 1
            column = 1
            continue

        if special_character(current_character):
            new_token = Token("SPECIAL", current_character, line, column)
            list_of_tokens.append(new_token)
            position = position + 1
            column = column + 1
            continue
            
        else:
            text = ""
            start_line = line
            start_column = column
            token_type = "UNCLASSIFIED"

            while position <len(thing_to_tokenize):
                current_character = thing_to_tokenize[position]
                
                if (special_character(current_character) or
                    current_character.isspace()):
                    break
                
                if current_character.isalpha():
                    text = text + current_character.upper()
                    
                else:
                    text = text + current_character
                    
                position = position + 1
                column = column + 1

            new_token = Token(token_type, text, start_line, start_column)
            list_of_tokens.append(new_token)

    return list_of_tokens


                

def classify(content_to_classify):

    list_of_tokens = []

    for index, token in enumerate(content_to_classify):
        if token.token_type == "SPECIAL":
            token_type = "UNKNOWN"
            token_subtype = "SPECIAL"
            
            if token.actual_text in SPECIAL_LOOKUP:
                token_type = "SPECIAL"
                token_subtype = SPECIAL_LOOKUP[token.actual_text]["token_subtype"]

            new_token = Token(token_type,
                              token.actual_text,
                              token.line_number,
                              token.column_number,
                              token_subtype)

            list_of_tokens.append(new_token)
            
            continue
        
        if token.actual_text[0].isalpha():
            
            token_type = "WORD"
            token_subtype = None
            
            if token.actual_text in KEYWORD_LOOKUP_SUBTYPE:
                token_type = "KEYWORD"
                token_subtype = KEYWORD_LOOKUP_SUBTYPE[token.actual_text]
                
            if (len(token.actual_text) > 1 and
                token.actual_text[len(token.actual_text)-1] == "-"):
                token_type = "UNKNOWN"
                
            new_token = Token(token_type,
                              token.actual_text,
                              token.line_number,
                              token.column_number,
                              token_subtype)
            list_of_tokens.append(new_token)
            
            continue
        
        if token.actual_text[0] == "-":
            if len(token.actual_text) == 1:
                new_token = Token("KEYWORD_OPERATOR",
                                  token.actual_text,
                                  token.line_number,
                                  token.column_number,
                                  "MINUS")
                
            elif token.actual_text[1].isdigit():
                new_token = Token("NUMBER",
                                  token.actual_text,
                                  token.line_number,
                                  token.column_number)
                
            else:
                new_token = Token("UNKNOWN",
                                  token.actual_text,
                                  token.line_number,
                                  token.column_number)
                
            list_of_tokens.append(new_token)
            
            continue
        
        if token.actual_text.isdigit():
            new_token = Token("NUMBER",
                              token.actual_text,
                              token.line_number,
                              token.column_number)
            
            list_of_tokens.append(new_token)
            
            continue
        
        else:
            new_token = Token("UNKNOWN",
                              token.actual_text,
                              token.line_number,
                              token.column_number)
            
            list_of_tokens.append(new_token)

    return list_of_tokens

SPLIT_LIST = ["PARAGRAPH", "OVERVIEW", "AREA", "INFORMATION", "CLASS"]
SINGLE_SPLIT = ["OVERVIEW"]
CONSUMES_PERIOD = ["TODO"]

def should_i_split(tokens, current_index, offset=1):
    
    current = current_index
    peek = current_index + offset
    peek_again = current_index + offset + 1
    
    if peek < len(tokens):
        next_token = tokens[peek]
        if tokens[current].actual_text in SINGLE_SPLIT:
            return next_token.actual_text == "."
        
    if peek_again < len(tokens):
        next_token = tokens[peek]
        further_token = tokens[peek_again]
        if next_token.actual_text in SPLIT_LIST:
            return further_token.actual_text == "."
        
    return False

def consume_period(tokens, current_index, offset=1):

    current = current_index
    peek = current_index + offset

    if peek <len(tokens):
        next_token = tokens[peek]
        if tokens[current].actual_text in CONSUMES_PERIOD:
            return next_token.actual_text == "."
    
    return False

def create_indent_token(indent, line, column):
    token_type = "INDENTATION"
    actual_text = ""
    line_number = line
    column_number = column
    token_subtype = False
    
    if indent == True:
        actual_text = "(("
        token_subtype = "INDENT"

    if indent == False:
        actual_text = "))"
        token_subtype = "DEDENT"
        
    return Token(token_type,
                 actual_text,
                 line_number,
                 column_number,
                 token_subtype,
                 False)

def find_functions(content_to_parse):

    functions = []
    current_function = []
    position = 0
    
    for position, token in enumerate(content_to_parse):
        if should_i_split(content_to_parse, position):
            # if I SHOULD split
            if current_function: # checks if items in list
                # if the list is empty, it returns "false"
                # so a list is only appended if it isn't empty
                functions.append(current_function)
            current_function = [token]
            # now start a new list on the current token

        else: # if I don't need to split
            current_function.append(token)
            # add current token to list

    if current_function: # add final function
        functions.append(current_function)
        
    return functions

def bundle_functions(content_to_parse):

    stream_of_tokens = []
    rejected_contents = []

    for current_list in content_to_parse:
        
        current_function = []
        index = 0

        while index < len(current_list):

            if len(current_list) < 4:
                rejected_contents.append(current_list[index])
                
                index = index + 1

            elif (current_list[index].actual_text == "OVERVIEW" and
                  should_i_split(current_list, index)):
                
                identifier_token = current_list[index]
                period_token = current_list[index+1]
                    

                new_token = Token("FUNCTION",
                                  identifier_token.actual_text,
                                  identifier_token.line_number,
                                  identifier_token.column_number,
                                  "MAIN",
                                  True)
                current_function.append(new_token)

                indent_token = create_indent_token(True,
                    identifier_token.line_number,
                    identifier_token.column_number)
                current_function.append(indent_token)

                index = index + 2
                
            elif should_i_split(current_list, index):
                
                identifier_token = current_list[index]
                keyword_token = current_list[index+1].actual_text
                period_token = current_list[index+2]

                new_token = Token("FUNCTION",
                    identifier_token.actual_text,
                    identifier_token.line_number,
                    identifier_token.column_number,
                    keyword_token,
                    True)
                current_function.append(new_token)

                indent_token = create_indent_token(True,
                    identifier_token.line_number,
                    identifier_token.column_number)
                current_function.append(indent_token)

                index = index + 3

            elif consume_period(current_list, index):

                identifier_token = current_list[index]
                period_token = current_list[index+1]

                new_token = Token("FUNCTION",
                    identifier_token.actual_text,
                    identifier_token.line_number,
                    identifier_token.column_number,
                    identifier_token.token_subtype,
                    True)
                current_function.append(new_token)

                index = index + 2
                
            else:
                current_function.append(current_list[index])
                index = index + 1
                
        if current_function:
            indent_token = create_indent_token(False,
                    0,
                    0)
            current_function.append(indent_token)
            stream_of_tokens.append(current_function)

    if len(rejected_contents) > 5:
        rejected_text = [token.actual_text for token in rejected_contents]
        raise ValueError(f"Too many rejected tokens: {rejected_text}")

    return stream_of_tokens

def sort_bundled_functions_clearly(bundled_functions):
    imports = []
    classes = []
    functions = []
    main = []

    for function_list in bundled_functions:
        function_token = function_list[0]
        function_type = function_token.token_subtype

        if function_type == "IMPORT":
            imports.append(function_list)
        elif function_type == "CLASS":
            classes.append(function_list)
        elif function_type == "PARAGRAPH":
            functions.append(function_list)
        elif function_type == "MAIN":
            main.append(function_list)

    sorted_functions = []
    sorted_functions.extend(imports)
    sorted_functions.extend(classes)
    sorted_functions.extend(functions)
    sorted_functions.extend(main)

    return sorted_functions
    
        
def format_contents(content_to_format):

    formatted_contents = []

    for current_list in content_to_format:

        position = 0
        indentation = 0

        while position < len(current_list):

            current = current_list[position]

            if current.token_subtype == "MAIN":
                text = "\ndef main():\n"

                new_token = TokenFormatter(text, indentation)
                formatted_contents.append(new_token)

                position = position + 1
                continue

            if current.token_subtype == "PARAGRAPH":

                index = 0
                sanitized_name = ""
                    
                while index < len(current.actual_text):
                    letter = current.actual_text[index]
                    if letter == "-":
                        sanitized_name = sanitized_name + "_"
                        index = index + 1
                    else:
                        sanitized_name = sanitized_name + letter.lower()
                        index = index + 1
                
                text = f"\ndef {sanitized_name}():\n"

                new_token = TokenFormatter(text, indentation)
                formatted_contents.append(new_token)

                position = position + 1
                continue

            if current.token_subtype == "INDENT":
                
                indentation = indentation + 1
                position = position + 1
                continue

            if current.token_subtype == "DEDENT":
                
                if indentation >= 1:
                    indentation = indentation - 1
                else:
                    indentation = 0
                    
                position = position + 1
                continue

            if current.token_subtype == "PASS":
                text = "pass\n"

                new_token = TokenFormatter(text, indentation)
                formatted_contents.append(new_token)

                position = position + 1
                continue

            else:
                print(cry)

    return formatted_contents
            

def main():
    verbose_python = load_verbose_python("basic-verbose-python.txt")
    tokenized_python = tokenize(verbose_python)
    classified_python = classify(tokenized_python)
    functional_python = find_functions(classified_python)
    #print(functional_python)   
    bundled_python = bundle_functions(functional_python)
 
    print(bundled_python)

    print("\n===FORMATTING CONTENTS===\n")

    sorted_python = sort_bundled_functions_clearly(bundled_python)
    print(sorted_python)

    print("\n===FORMATTING CONTENTS===\n")
    formatted_python = format_contents(sorted_python)
    print(formatted_python)

    
    joined_python = " ".join(token.actual_text for token in formatted_python)
    print(joined_python)
    
    write_useable_python(joined_python, "converted-to-pyhon.py")

if __name__ == "__main__":
    main()
