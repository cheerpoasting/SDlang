# Imports. 
from Node_Token_Stuff import *
from Lookups import *

# Open/Read Files. 
def open_file(file_name):

    with open(file_name, 'r') as file:
        contents = file.read()

    return contents

# Parse Lexed Tokens.

def peek(tokens, position, amount=1):

    position += amount
    
    if 0 <= (position) < len(tokens):
        return tokens[position]

program = ProgramNode()

def parse_tokens(lexed_tokens):

    token_index = 0

    global current_paragraph
    current_paragraph = None
    
    while token_index < len(lexed_tokens):
        
        if isinstance(lexed_tokens[token_index], CommentToken):

            #comment_node = CommentNode(lexed_tokens[token_index].text)
            #current_paragraph.add_child(comment_node)

            #print("comment appended")
            token_index += 1
            continue
        
        if lexed_tokens[token_index].text in KEYWORD_LOOKUP:
            #print (f"found Keyword! {lexed_tokens[token_index].text}")
            if lexed_tokens[token_index].text == "OVERVIEW":
                main_node = ParagraphNode("MAIN")
                program.add_child(main_node)

                print("added main node")
                current_paragraph = main_node
                token_index += 1
                continue
            
            if lexed_tokens[token_index].text == "PARAGRAPH":
                #print("found PARAGRAPH")
                function_name = peek(lexed_tokens, token_index, -1)
                went_check = peek(lexed_tokens, token_index, -3)
                
                if went_check.text == "WENT":

                    call_node = CallNode(function_name.text)
                    current_paragraph.add_child(call_node)
                    
                    #print(f"appended call {function_name.text} to {current_paragraph.name}")
                    token_index += 1
                    continue
                
                else:
                    new_node = ParagraphNode(function_name.text)
                    program.add_child(new_node)

                    #print (f"added {function_name.text} node")
                    current_paragraph = new_node
                    token_index += 1
                    continue
                
            if lexed_tokens[token_index].text == "TODO":

                period = peek(lexed_tokens, token_index)

                if period.text == ".":
                    function_node = FunctionNode("PASS")
                    current_paragraph.add_child(function_node)

                    #print(f"PASS added to {current_paragraph}")
                    token_index += 1
                    continue
                else:
                    print(f"didn't find period")
                    token_index += 1
                    continue
            else:
                print(f"unhandled Keyword {{lexed_tokens[token_index].text}}")
                token_index += 1
                continue
        else:
            token_index += 1
            continue

# Main Program.

def main():

    raw_file = open_file("basic-verbose-python.txt")
    lexed_tokens = Lexer(raw_file).lex()
    print(f"{lexed_tokens}\n")
    
    parse_tokens(lexed_tokens)

    print(f"\nThe Program contains the following paragraphs:\n{program.get_children()}\n")

    i = 0

    while i < len(program.get_children()):
        
        main_node = program.get_children()[i]
        print(f"from {main_node} {main_node.get_children()}")

        i += 1
    

if __name__ == "__main__":
    main()
