from Main_Controller import *

# ACW -- NEXT STEP implement AST class, and node instructions for "parse_added"

source_content = read_source_file("file-to-be-parsed.sdlang")
lexed_content = tokenize(source_content)
classified_content = classify_tokens(lexed_content)

#A class to hold the basic parse functions like "peek" and "consume"

def parse_added(parser):
    print("you called parse added!")
    
KEYWORD_LOOKUP = {
    "KEYWORD_OPERATOR": {
        "ADDED": parse_added # no () or python would run the operation while reading this line
    }
}

class ParsingController:
    
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0


    # Manipulating Tokens.

    def peek(self):
        if self.current >= len(self.tokens):
            return None
        return self.tokens[self.current] # look at yourself

    def look_ahead(self):
        if self.current + 1 >= len(self.tokens): 
            return None
        return self.tokens[self.current+1] # look at next token

    def consume(self):
        token = self.peek()
        if token:
            self.current += 1 # advance to next token
        return token


    # Finding And Using Parsing Functions. 

    def lookup_keyword(self, token):
        # helper function for the main "parse" function
        if token.token_type in KEYWORD_LOOKUP:
            if token.actual_text in KEYWORD_LOOKUP[token.token_type]:
                return KEYWORD_LOOKUP[token.token_type][token.actual_text]
                # this returns the OBJECT of the function for which
                # "token.actual_text" is the KEY
        return None # implicit "else" because the IF has its own return

    def parse_expression(self):
        token = self.peek()
        parse_function = self.lookup_keyword(token)

        if parse_function:
            return parse_function(self)
        else:
            raise Exception(f"I don't know how to parse {token.actual_text}")

parser = ParsingController(classified_content)

result = parser.parse_expression()
