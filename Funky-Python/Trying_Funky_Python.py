class Token:
    def __init__ (self, token_type, actual_text, line_number, column_number):
        self.token_type = token_type
        self.actual_text = actual_text
        self.line_number = line_number
        self.column_number = column_number

    def __str__(self): # how it automatically represents itself as a string
        return f"{self.actual_text}"

    def __repr__(self): # how it appears in a list
        return f"{self.token_type} \"{self.actual_text}\" L{self.line_number}C{self.column_number}\n"

def load_verbose_python(file_name):
    with open(file_name, 'r') as file:
        verbose_python = file.read()
        return verbose_python

def write_useable_python(content_to_save, file_name):
    with open(file_name, 'w') as file:
        file.write(content_to_save)

#def translate(content_to_translate):
#tokenize
#classify
#parse

# "normalize" content at some point

def special_character(input_thing):
    if not input_thing.isalnum() and input_thing != "-" and input_thing !="'":
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
                if special_character(current_character) or current_character.isspace():
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

KEYWORD_LOOKUP_TYPE = {
    "OVERVIEW": "KEYWORD_MAIN",
    "PASS": "KEYWORD_FUNCTION"
}

KEYWORD_LOOKUP_ARGUMENTS = {
    "OVERVIEW": {
        "NUMBER": 1,
        "STRUCTURE": ["PERIOD"]
    },
    "PASS": {
        "NUMBER": 2,
        "STRUCTURE": ["OVER", "PERIOD"]
    }
}

SPECIAL_LOOKUP = {
    "@": {
        "token_type": "SYMBOL",
        "actual_text": "AT-SIGN"
    },
    ".": {
        "token_type": "PUNCTUATION",
        "actual_text": "PERIOD"
    }
}
                

def classify(content_to_classify):

    list_of_tokens = []

    for index, token in enumerate(content_to_classify):
        if token.token_type == "SPECIAL":
            token_type = "UNKNOWN_SPECIAL"
            token_text = token.actual_text
            if token_text in SPECIAL_LOOKUP:
                token_type = SPECIAL_LOOKUP[token.actual_text]["token_type"]
                token_text = SPECIAL_LOOKUP[token.actual_text]["actual_text"]
            new_token = Token(token_type, token_text, token.line_number, token.column_number)
            list_of_tokens.append(new_token)
            continue 
        if token.actual_text[0].isalpha():
            token_type = "WORD"
            if token.actual_text in KEYWORD_LOOKUP_TYPE:
                token_type = KEYWORD_LOOKUP_TYPE[token.actual_text]
            if len(token.actual_text) > 1 and token.actual_text[len(token.actual_text)-1] == "-":
                token_type = "UNKNOWN"
            new_token = Token(token_type, token.actual_text, token.line_number, token.column_number)
            list_of_tokens.append(new_token)
            continue
        
        if token.actual_text[0] == "-":
            if len(token.actual_text) == 1:
                new_token = Token("KEYWORD_OPERATOR", "MINUS", token.line_number, token.column_number)
            elif token.actual_text[1].isdigit():
                new_token = Token("NUMBER", token.actual_text, token.line_number, token.column_number)
            else:
                new_token = Token("UNKNOWN", token.actual_text, token.line_number, token.column_number)
            list_of_tokens.append(new_token)
            continue
        
        if token.actual_text.isdigit():
            new_token = Token("NUMBER", token.actual_text, token.line_number, token.column_number)
            list_of_tokens.append(new_token)
            continue
        
        else:
            new_token = Token("UNKNOWN", token.actual_text, token.line_number, token.column_number)
            list_of_tokens.append(new_token)

    return list_of_tokens
            

def lex(content_to_lex):
    pass

def parse(content_to_parse):
    pass

def main():
    verbose_python = load_verbose_python("basic-verbose-python.txt")
    tokenized_python = tokenize(verbose_python)
    classified_python = classify(tokenized_python)
    
    print(classified_python)
    
#    write_useable_python(translated_python, "converted-to-pyhon.py")

if __name__ == "__main__":
    main()
