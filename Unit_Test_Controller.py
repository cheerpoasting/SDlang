import os
import tempfile

from Main_Controller import *

# Initial File Opening.
def test_initial_file_reading():

    print("⚡ Testing File Reading -- read_source_file(Correct_Filepath)")
    test_nickname = "test_initial_file_reading"
    
    # First, create a temporary test file
    test_contents = "Hello, this is test content!\nLine 2\nLine 3"
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', delete=False, suffix='.sdl') as temp_file:
        temp_file.write(test_contents)
        temp_file_path = temp_file.name

    # Test the function here
    try: 
        result = read_source_file(temp_file_path)
        if result == test_contents:
            print(f"✅ {test_nickname} PASSED\n")
            return True
        else:
            print(f"💩 {test_nickname} FAILED: content doesn't match")
            print(f"Expected: {test_content}")
            print(f"Got: {result}\n")
            return False

    # Get rid of the temporary file
    finally:
        os.unlink(temp_file_path)

# Test how the program will react if the file isn't found.
def test_reading_nonexistent_file():

    print("⚡ Testing File Reading -- read_source_file(FileNotFound)")
    test_nickname = "test_reading_nonexistent_file"
    
    # We don't need to make a file, because the point is not to find one
    fake_path = "nonexistant_file.txt"

    try:
        result = read_source_file(fake_path)
        print(f"💩 {test_nickname} FAILED: should have exited\n.")
        return False
    except SystemExit as error_code:
        # Check if it exited with the right error code
        if str(error_code) == "SDL-E404":
            print(f"✅ {test_nickname} PASSED: correctly exited with SDL-E404\n")
            return True
        else:
            print(f"💩 {test_nickname} FAILED: wrong exit code: {error_code}\n")
            return False
    except Exception as error_code:
        print(f"💩 {test_nickname} FAILED: unexpected error: {error_code}\n")
        return False

# Test how the program will react if the initial file is empty.
def test_initial_file_is_empty():

    print("⚡ Testing File Reading -- read_source_file(FileEmpty)")
    test_nickname = "test_initial_file_is_empty"

    # We need to create a test file
    empty_contents = "" # will make the file empty
    
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', delete=False, suffix='.sdl') as empty_file:
        empty_file.write(empty_contents)
        empty_file_path = empty_file.name

    # Test the function here
    try:
        result = read_source_file(empty_file_path)
        print(f"💩 {test_nickname} FAILED: should have exited\n.")
        return False
    except SystemExit as error_code: #SystemExit is what "sys.exit()" gives
        if str(error_code) == "SDL-E002":
            print(f"✅ {test_nickname} PASSED: correctly exited with {error_code}\n")
            return True
        else:
            print(f"💩 {test_nickname} FAILED: unexpected error: {error_code}\n")
            return False
    
    # Get rid of the temporary file
    finally: # still part of the try block
        os.unlink(empty_file_path)
        
# Test how the program will act if the encoding is not the expected one.
def test_unexpected_encoding():

    print("⚡ Testing File Reading -- read_source_file(unexpected_encoding)")
    test_nickname = "test_unexpected_encoding"

    # We need to create a test file
    wrongly_encoded_contents = "This file has a smart quote: …" # this elipse character is not utf-8
    
    with tempfile.NamedTemporaryFile(mode='w', encoding='windows-1252', delete=False, suffix='.sdl') as wrongly_encoded_file:
        wrongly_encoded_file.write(wrongly_encoded_contents)
        wrongly_encoded_file_path = wrongly_encoded_file.name

    # Test Function Here
    try:
        result = read_source_file(wrongly_encoded_file_path)
        print(f"💩 {test_nickname} FAILED: should have exited\n.")
        return False
    except SystemExit as error_code: #SystemExit is what "sys.exit()" gives
        if str(error_code) == "SDL-E001":
            print(f"✅ {test_nickname} PASSED: correctly exited with {error_code}\n")
            return True
        else:
            print(f"💩 {test_nickname} FAILED: unexpected error: {error_code}\n")
            return False
    
    # Get rid of the temporary file
    finally: # still part of the try block
        os.unlink(wrongly_encoded_file_path)

# Test how the program will act if a file has a wrong extension.
def test_file_has_wrong_extension():

    print("⚡ Testing File Reading -- read_source_file(FileWithWrongExtension)")
    test_nickname = "test_file_has_wrong_extension"

    # We need to create a test file
    contents = "This should have an incorrect file extension" # we make a random file
    
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', delete=False) as wrong_extension_file:
        wrong_extension_file.write(contents)
        wrong_extension_path = wrong_extension_file.name

    # Test the function here
    try:
        result = read_source_file(wrong_extension_path)
        print(f"💩 {test_nickname} FAILED: should have exited\n.")
        return False
    except SystemExit as error_code: #SystemExit is what "sys.exit()" gives
        if str(error_code) == "SDL-E003":
            print(f"✅ {test_nickname} PASSED: correctly exited with {error_code}\n")
            return True
        else:
            print(f"💩 {test_nickname} FAILED: unexpected error: {error_code}\n")
            return False

def test_file_has_no_extension():

    print("⚡ Testing File Reading -- read_source_file(FileWithNoExtension)")
    test_nickname = "test_file_has_no_extension"

    # We need to create a test file
    contents = "This should have an no file extension" # we make a random file
    
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', delete=False, suffix='.md') as no_extension_file:
        no_extension_file.write(contents)
        no_extension_path = no_extension_file.name

    # Test the function here
    try:
        result = read_source_file(no_extension_path)
        print(f"💩 {test_nickname} FAILED: should have exited\n.")
        return False
    except SystemExit as error_code: #SystemExit is what "sys.exit()" gives
        if str(error_code) == "SDL-E003":
            print(f"✅ {test_nickname} PASSED: correctly exited with {error_code}\n")
            return True
        else:
            print(f"💩 {test_nickname} FAILED: unexpected error: {error_code}\n")
            return False
    
    # Get rid of the temporary file
    finally: # still part of the try block
        os.unlink(no_extension_path)


############# TESTING LEXER HERE #####################################


def test_number_of_tokens():

    print("⚡ Testing Tokenizer -- tokenize(how_many)")
    test_nickname = "test_number_of_tokens"

    # Create Temp File

    contents = "3 dog 3b b3 added"

    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', delete=False, suffix='.txt') as tokenize_constants_file:
        tokenize_constants_file.write(contents)
        tokenize_constants_path = tokenize_constants_file.name

    # Test Function Here

    source_code = read_source_file(tokenize_constants_path)
    lexed_content = tokenize(source_code)

    if len(lexed_content) != 5:
        print(f"💩 {test_nickname} FAILED: There should have been 5 tokens, but I found {len(lexed_content)}\n")
        return False

    print(f"✅ {test_nickname} PASSED: there were the number of tokens I expected \n")
    return True

def test_single_token(text): # helper function to create tokens
    token = Token("UNCLASSIFIED", text, 1, 1)
    classified = classify_tokens([token])
    return classified[0]

def test_token_types():
    print("⚡ Testing Tokenizer -- tokenize(the_types)")
    test_nickname = "test_token_types"

    checked_tokens = 0
    correct_tokens = 0

    dictionary_of_tokens = {
        "DOG": "WORD",
        "ADDED": "KEYWORD_OPERATOR",
        "5": "NUMBER",
        "3A": "UNKNOWN",
        "A2": "UNKNOWN"
    }

    for input_text, expected_type in dictionary_of_tokens.items():
        actual_result = test_single_token(input_text)
        if actual_result.token_type == expected_type.upper():
            correct_tokens = correct_tokens + 1
        else:
            print(f"{input_text} was {actual_result.token_type} instead of {expected_type}")
        checked_tokens = checked_tokens + 1

    if checked_tokens == correct_tokens:
        print(f"✅ {test_nickname} PASSED: each token was what I expected \n")
        return True
    else:
        return False
    
#######################################################################

        # FINAL LOGICAL OPERATIONS OF THE TEST SUITE

#######################################################################



def choose_emoji(tests_passed, tests_run):
    emoji_result = (tests_passed/tests_run)
    if emoji_result == 1:
        return "🎁"
    elif emoji_result < 0.5:
        return "💩"
    else:
        return "😭"        
    

def run_tests(): # place the name of every test here
    tests = [
        test_initial_file_reading,
        test_reading_nonexistent_file,
        test_initial_file_is_empty,
        test_unexpected_encoding,
        test_file_has_wrong_extension,
        test_file_has_no_extension,
        test_number_of_tokens,
        test_token_types
    ]
    
    passed = 0
    for test in tests:
        if test():
            passed += 1

    emoji_result = choose_emoji(passed, len(tests))

    print(f"\n{emoji_result} {passed}/{len(tests)} tests passed {emoji_result}")

if __name__ == "__main__":
    run_tests()
