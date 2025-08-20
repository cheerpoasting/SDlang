from Main_Controller import *

source_content = read_source_file("file-to-be-parsed.sdlang")
lexed_content = tokenize(source_content)
classified_content = classify_tokens(lexed_content)

def display_initial_tokens(tokens, description):
    print(description)
    for index, token in enumerate(tokens): # enumerate gives both position
        # and content
        if index == len(tokens) - 1: # needs to be len - 1 because there
            # might be 3 tokens, but indexing starts at 0
            print(f"└── {token.token_type}: {token.actual_text} (L{token.line_number}C{token.column_number})")
        else:
            print(f"├── {token.token_type}: {token.actual_text} (L{token.line_number}C{token.column_number})")
        

display_initial_tokens(classified_content, "Initial tokens")

def remove_unknown_tokens(tokens):
    removed_list = []
    clean_tokens = []
    for token in tokens:
        if token.token_type == "UNKNOWN":
            removed_list.append(token.actual_text)
        else:
            clean_tokens.append(token)
    return clean_tokens, removed_list

good_tokens, unknown_names = remove_unknown_tokens(classified_content)

input() # you have to hit a key to continue to the next step

if len(unknown_names) > 0:
    display_initial_tokens(good_tokens, f"\nRemoved UNKNOWN elements {unknown_names}")
else:
    print("\nChecked for UNKNOWN elements, none found")

##So, first we want to parse through and find a keyword.
##Then, based on the keyword, we find the instruction pattern
##So then we take the arguments, and group them.
##
##that means we take the keyword "added" and we "subtree" "3 to 5"
##because "3, to, 5" are the arguments of "added".


##so first i should go through the tokens until I see a keyword
##i should make it a node, and sub everything underneath it.

input() # you have to hit a key to continue to the next step

KEYWORD_LOOKUP = {
    "K": { # First Letter
        "KEYWORD_OPERATOR": {
            "ADDED": {
                "consume": 3, # number so it will return as int
                "pattern": ["NUMBER", "TO", "NUMBER"]
            },
        },
        "KEYWORD_CONTEXTUAL": {
            "TO": {
                "consume": 0,
                "pattern": None
            }
        }
    }
}

def display_tree(tokens, description, lookup_results=None):
    # code to display the tree at various levels of existing
    # level is the "step" we are on.
    print(description)
    for index, token in enumerate(tokens):
        if index == len(tokens)-1:
            print(f"└── {token.token_type}: {token.actual_text} (L{token.line_number}C{token.column_number})")
        else:
            print(f"├── {token.token_type}: {token.actual_text} (L{token.line_number}C{token.column_number})")

        if lookup_results and lookup_results[index] is not None:
            if index == len(tokens) - 1:
                print(f"    └── {lookup_results[index]}")
            else:
                print(f"│   └── {lookup_results[index]}")
            
display_tree(good_tokens, "Basal Tree")

input() # you have to hit a key to continue to the next step

def initial_lookup(tokens):
    # code to look up first letter of token_type
    # all keywords and identifiers should show token letter
    results = []
    for each in tokens:
        first_letter = each.token_type[0]
        if first_letter == "K":
            if first_letter in KEYWORD_LOOKUP:
                results.append(f"{first_letter}")
            else:
                results.append(f"{first_letter} not found")
        else:
            results.append(None)
    return results

step_one = initial_lookup(good_tokens)

display_tree(good_tokens, "First Step", step_one)

input() # you have to hit a key to continue to the next step

def keyword_type_lookup(tokens):
    # code to look up keyword_type of token
    # all keywords and identifiers whould show token type
    results = []
    for each in tokens:
        first_letter = each.token_type[0]
        if first_letter == "K":
            if each.token_type in KEYWORD_LOOKUP[first_letter]:
                results.append(f"{each.token_type}")
            else:
                results.append(f"{each.token_type} not found")
        else:
            results.append(None)
    return results

step_two = keyword_type_lookup(good_tokens)

display_tree(good_tokens, "Second Step", step_two)

input() # you have to hit a key to continue to the next step

def keyword_rules_lookup(tokens):
    # code to lookup keyword ("added") and apply the rules
    # all "arguments" should become children now
    results = []
    for index, each in enumerate(tokens):
        first_letter = each.token_type[0]
        if first_letter == "K":
            if each.actual_text in KEYWORD_LOOKUP[first_letter][each.token_type]:
                consume_count = KEYWORD_LOOKUP[first_letter][each.token_type][each.actual_text]["consume"]
                if consume_count > 0:
                    consumed_tokens = []
                    for i in range(1, consume_count + 1):
                        if index + i < len(tokens):
                            consumed_tokens.append(tokens[index + i].actual_text)
                    results.append(f"{each.actual_text} will consume {consume_count} tokens: {consumed_tokens}")
                else: 
                    results.append(f"{each.actual_text}")
            else:
                results.append(f"{each.actual_text} not found")
        else:
            results.append(None)
    return results

step_three = keyword_rules_lookup(good_tokens)

display_tree(good_tokens, "Third_Step", step_three)

input() # you have to hit a key to continue to the next step
    
class ParentNode():
    def __init__(self, token):
        self.token = token # parent node
        self.arguments_consumed = []

    def add_child(self, consumed_argument): # add one
        self.arguments_consumed.append(consumed_argument)

    def add_children(self, consumed_arguments): # add many
        for argument in consumed_arguments:
            self.arguments_consumed.append(argument)

def consume_tokens(tokens):
    parent_nodes = []
    for index, each in enumerate(tokens):
        first_letter = each.token_type[0]
        if first_letter == "K":
            if each.actual_text in KEYWORD_LOOKUP[first_letter][each.token_type]:
                consume_count = KEYWORD_LOOKUP[first_letter][each.token_type][each.actual_text]["consume"]
                if consume_count > 0:
                    parent = ParentNode(each)
                    for i in range(1, consume_count + 1):
                        if index + i < len(tokens):
                            parent.add_child(tokens[index+i])
                            #adds each indexed token as child
                        else:
                            pass
                    parent_nodes.append(parent)
                else: 
                    pass
            else:
                pass
        else:
            pass
    return parent_nodes

catch_parent_nodes = consume_tokens(good_tokens)


def display_parse_tree(parent_nodes, description):
    print(description)
    for index, parent in enumerate(parent_nodes):
        # Display the parent node
        if index == len(parent_nodes) - 1:
            print(f"└── {parent.token.token_type}: {parent.token.actual_text} (L{parent.token.line_number}C{parent.token.column_number})")
            child_prefix = "    "
        else:
            print(f"├── {parent.token.token_type}: {parent.token.actual_text} (L{parent.token.line_number}C{parent.token.column_number})")
            child_prefix = "│   "
        
        # Display the child nodes
        for child_index, child in enumerate(parent.arguments_consumed):
            if child_index == len(parent.arguments_consumed) - 1:
                print(f"{child_prefix}└── {child.token_type}: {child.actual_text} (L{child.line_number}C{child.column_number})")
            else:
                print(f"{child_prefix}├── {child.token_type}: {child.actual_text} (L{child.line_number}C{child.column_number})")

display_parse_tree(catch_parent_nodes, "Parse Tree with Children")
##def look_for_first_letter(token):
##    first_letter = token.token_type[0]
##    if first_letter in KEYWORD_LOOKUP:
##        results = KEYWORD_LOOKUP[first_letter]
##        #print(f"{first_letter}: {list(results.keys())}")
##        return results
##    else:
##        print(f"I didn't find {first_letter}")
##        return None
##
##first_result = look_for_first_letter(good_tokens[0])
##
##def display_token_lookups(tokens, description, lookup_token_index=None):
##    print(description)
##    for index, token in enumerate(tokens):
##        if index == len(tokens) - 1:
##            print(f"└── {token.token_type}: {token.actual_text} (L{token.line_number}C{token.column_number})")
##        else:
##            print(f"├── {token.token_type}: {token.actual_text} (L{token.line_number}C{token.column_number})")
##        
##        # Only show lookup for the specified token
##        if index == lookup_token_index:
##            lookup_result = look_for_first_letter(token)
##            if lookup_result:
##                first_letter = token.token_type[0]
##                if index == len(tokens) - 1:
##                    print(f"    └── {first_letter}: {list(lookup_result.keys())}")
##                else:
##                    print(f"│   └── {first_letter}: {list(lookup_result.keys())}")
##
##
##display_token_lookups(good_tokens, "Tokens with first lookup", lookup_token_index=0)
##
##def look_for_keyword(token, first_level_result):
##    keyword_type = token.token_type
##    if keyword_type in first_level_result:
##        results = first_level_result[keyword_type]
##        # print(f"{keyword_type}: {list(results.keys())}")
##        return results
##    else:
##        print(f"I didn't find {keyword_type}")
##        return None
##
##second_result = look_for_keyword(good_tokens[0], first_result)

##look_for_first_letter(good_tokens[0])# pass only the first token!
##
##class ParseNode:
##    def __init__(self, token):
##        self.value = token.actual_text  # "ADDED", "3", "to", "5"
##        self.token = token             # keeps the full token for debugging
##        self.children = []             # list of child ParseNodes
##    
##    def add_child(self, child_node):
##        self.children.append(child_node)
##
##def initial_tree_structure(tokens):
##    keyword_token = tokens[0]
##
##    first_letter = keyword_token.token_type[0] # first letter of token type
##    token_type = keyword_token.token_type # now search under "K" for keyword type
##    keyword = keyword_token.actual_text # now find the specific keyword
##
##    rule = KEYWORD_LOOKUP[first_letter][token_type][keyword]
##
##    consume_count = rule["consume"]
##    arguments = tokens[1:1+consume_count] # index slicing is NOT inclusive at the end
##    # this means that 1+3 = 4, so we take from token 1 "tokens [1:
##    # then we go UNTIL token 4 ":4]" but NOT including the 4th one
##
##    root = ParseNode(keyword_token) # keeps whole token intact for debugging
##
##    for each in arguments:
##        root.add_child(ParseNode(each))
##
##    return root
##        
##def display_parse_tree(node, description, prefix="", is_last=True):
##    if prefix == "":
##        print(description)
##
##    connector = "└── " if is_last else "├── "
##    print(f"{prefix}{connector}{node.value}")
##
##    for index, child in enumerate(node.children):
##        is_last_child = (index == len(node.children) - 1)
##        child_prefix = prefix + ("    " if is_last else "│   ")
##        display_parse_tree(child, "", child_prefix, is_last_child)
##
##
##parse_tree = initial_tree_structure(good_tokens)
##display_parse_tree(parse_tree, "Went Through Arguments")

