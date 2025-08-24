# Token Class

class Token:
    def __init__(self, actual_text, line, column,
                 token_type="UNCLASSIFIED",
                 token_subtype="",
                 consumed=False, indentation=0, print_text=""):
        self.actual_text = actual_text
        self.line = line
        self.column = column
        self.token_type = token_type
        self.subtype = token_subtype
        self.consumed = consumed
        self.indentation = indentation
        self._print_text = print_text
    
    def __str__(self):
        return f"\"{self.actual_text}\""
    
    def __repr__(self):
        return f"\"{self.actual_text}\"\n\t\tL{self.line}C{self.column}\t{self.token_type}_{self.subtype}_{self.consumed}\n"

    @property
    def print_text(self):
        if self._print_text:
            return ("    " * self.indentation) + self._print_text
        else:
            return "invalid assignment"
    

# Lookup Tables.

KEYWORD_LOOKUP = {
    "OVERVIEW": "MAIN",
    "WENT": "CALL",
    "PARAGRAPH": "PARAGRAPH",
    "TODO": "PASS",
    "TO": "CONTEXTUAL"
}

SYMBOL_LOOKUP = {
    ".": "PERIOD"
}


# Helper Functions.

def special_character(character):
    if (character.isspace() or
        character.isalnum() or
        character == "-"):
        return False
    return True # otherwise return true

def advance_character(position, column):
    position = position + 1
    column = column + 1
    return position, column
    

# Tokenize Stream.

def make_tokens(stream):

    list_of_tokens = []

    position = 0
    line = 1
    column = 1

    while position < len(stream):
        
        character = stream[position]

        if character == " " or character == "\t":
            position, column = advance_character(position, column)
            continue

        elif character == "\n":
            position = position + 1
            line = line + 1
            column = 1
            continue

        elif special_character(character):

            new_token = Token(character, line, column, "SPECIAL")
            list_of_tokens.append(new_token)
            
            position, column = advance_character(position, column)

        else:
            starting_line = line
            starting_column = column

            text = ""

            while not (special_character(character)
                or character.isspace()):

                text = text + character.upper()

                position, column = advance_character(position, column)
                
                character = stream[position]

            new_token = Token(text, starting_line, starting_column)
            list_of_tokens.append(new_token)

    return list_of_tokens


# Classify Tokens.

def classify(contents):

    classified_contents = []

    for token in contents:

        # Is it a number?
        if token.actual_text.isdigit():
            new_token = Token(token.actual_text,
                token.line,
                token.column,
                "NUMBER")
            classified_contents.append(new_token)
            continue
        
        if token.actual_text in KEYWORD_LOOKUP:
            key = KEYWORD_LOOKUP[token.actual_text]
            new_token = Token(token.actual_text,
                token.line,
                token.column,
                "FUNCTION",
                key)
            classified_contents.append(new_token)
            continue

        if (token.actual_text[0].isalpha() and
            not token.actual_text[-1] == "-"):
            new_token = Token(token.actual_text,
                token.line,
                token.column,
                "WORD")
            classified_contents.append(new_token)
            continue

        if token.actual_text in SYMBOL_LOOKUP:
            symbol = SYMBOL_LOOKUP[token.actual_text]
            new_token = Token(token.actual_text,
                token.line,
                token.column,
                token.token_type,
                symbol)
            classified_contents.append(new_token)
            continue
        
        else:
            new_token = Token(token.actual_text,
                token.line,
                token.column,
                "UNKNOWN")
            classified_contents.append(token)
            continue

    return classified_contents

def tokenize(contents):
    raw_tokens = make_tokens(contents)
    return classify(raw_tokens)
