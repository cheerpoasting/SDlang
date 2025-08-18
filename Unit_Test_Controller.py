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

def test_tokenize_constants():

    print("⚡ Testing Tokenizer -- tokenize(just_constants)")
    test_nickname = "test_tokenize_constants"

    # Create Temp File

    contents = "3 3"

    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', delete=False, suffix='.txt') as tokenize_constants_file:
        tokenize_constants_file.write(contents)
        tokenize_constants_path = tokenize_constants_file.name

    # Test Function Here

    source_code = read_source_file(tokenize_constants_path)
    lexed_content = tokenize(source_code)

    if len(lexed_content) != 2:
        print(f"💩 {test_nickname} FAILED: There should have been 2 tokens, but I found {len(lexed_content)}")
        return False

    token1 = lexed_content[0]
    if (token1.type_of_token == "NUMBER" and
        token1.actual_text == "3" and
        token1.line_number == 1 and
        token1.column_number == 1):
        print("\tToken 1 Correct")
    else:
        print(f"💩 {test_nickname} FAILED: Token 1 was incorrect! Expected 'NUMBER \"3\", L1C1' but recieved {token1.type_of_token} \"{token1.actual_text}\", L{token1.line_number}C{token1.column_number}")
        return False

    token2 = lexed_content[1]
    if (token2.type_of_token == "NUMBER" and
        token2.actual_text == "3" and
        token2.line_number == 1 and
        token2.column_number == 3):
        print("\tToken 2 Correct")
    else:
        print(f"💩 {test_nickname} FAILED: Token 2 was incorrect! Expected 'NUMBER \"3\", L1C3' but recieved {token2.type_of_token} \"{token2.actual_text}\", L{token2.line_number}C{token2.column_number}")
        return False

    print(f"✅ {test_nickname} PASSED: Tokens are what I expected\n")
    return True

    
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
        test_tokenize_constants
    ]
    
    passed = 0
    for test in tests:
        if test():
            passed += 1

    emoji_result = choose_emoji(passed, len(tests))

    print(f"\n{emoji_result} {passed}/{len(tests)} tests passed {emoji_result}")

if __name__ == "__main__":
    run_tests()
