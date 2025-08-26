# Lexer.

class Lexer:
    def __init__(self, text):
        self.text = text
        self.position = 0
        self.line = 1
        self.column = 1
        self.character = None


    def lex(self):

        tokens = []

        while self.position < len(self.text):
            
            self.character = self.text[self.position]

            if self.character == "#":
                tokens.append(self.handle_comment_tokens())
                continue

            elif self.character == "\"":
                tokens.append(self.handle_string_tokens())
                continue

            elif self.character.isalnum()or self.character == "-":
                tokens.append(self.handle_general_tokens())
                continue
                
            elif not self.character.isspace():
                tokens.append(self.handle_special_tokens())
                continue
                
            else:
                self.advance()
                

        return tokens

    def handle_string_tokens(self):
        
        starting_line = self.line
        starting_column = self.column

        text = self.character
        self.advance()
        
        while self.position < len(self.text) and self.character != "\"":

            text += self.character

            self.advance()

        text += self.character
        self.advance()

        new_token = StringToken(text, starting_line, starting_column)

        return new_token

    def handle_comment_tokens(self):

        starting_line = self.line
        starting_column = self.column

        text = ""
        
        while self.position < len(self.text) and self.character != "\n":

            text += self.character

            self.advance()

        new_token = CommentToken(text, starting_line, starting_column)

        return new_token
            

    def handle_general_tokens(self):

        starting_line = self.line
        starting_column = self.column

        text = ""

        while (self.position < len(self.text) and
               (self.character.isalnum() or
                self.character == "-")):

            if self.character.isalpha():
                text += self.character.upper()
            else:
                text += self.character

            self.advance()

        new_token = GeneralToken(text, starting_line, starting_column)

        return new_token


    def handle_special_tokens(self):
        
        if self.position <len(self.text):
            
            new_token = SpecialToken(self.character, self.line, self.column)
            
            self.advance()

        return new_token

    def advance(self):
        
        if self.position < len(self.text):
            if self.text[self.position] == "\n":
                self.line += 1 
                self.column = 1
            else:
                self.column += 1
                
            self.position += 1

            
            if self.position < len(self.text):
                self.character = self.text[self.position]
            else:
                self.character = None

# Tokens.

    # Remember to check type using isinstance(token, token.type).
    # This is pythonic and has better error handling. 

class Token:
    
    def __init__(self, text, line, column):
        self.text = text
        self.line = line
        self.column = column
        self.type = "UNDEFINED"

    def __repr__(self):

        return f"{self.text}"

class StringToken(Token):

    def __init__(self, text, line, column):
        super().__init__(text, line, column)
        self.type = "STRING"

class CommentToken(Token):

    def __init__(self, text, line, column):
        super().__init__(text, line, column)
        self.type = "COMMENT"

    def __repr__(self):

        if len(self.text) <= 20:
            return f"{self.text}"
        if len(self.text) > 20:
            return f"{self.text[0:18]}--"

class SpecialToken(Token):

    def __init__(self, text, line, column):
        super().__init__(text, line, column)
        self.type = "SPECIAL"

class GeneralToken(Token):

    def __init__(self, text, line, column):
        super().__init__(text, line, column)
        self.type = "GENERAL"

# Parsing.

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def current_token(self):
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        return None

    def consume(self):
        if self.position + 1< len(self.tokens):
            self.position += 1
        return None

    def peek(self):
        if self.position + 1< len(self.tokens):
            return self.tokens[self.position + 1]


# Nodes. 

class Node:
    def __init__(self):
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)

    def get_children(self):
        return self.children
    

class ProgramNode(Node):
    def __init__(self):
        super().__init__()
        self.node_type = "PROGRAM"

class ParagraphNode(Node):
    def __init__(self):
        super().__init__()
        self.node_type = "PARAGRAPH"
        
