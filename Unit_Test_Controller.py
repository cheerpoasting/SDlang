import os
import tempfile

from Main_Controller import *

# Initial File Opening.
def test_initial_file_reading():

    print("⚡ Testing File Reading -- read_source_file(Correct_Filepath)")
    test_nickname = "test_initial_file_reading"
    
    # First, create a temporary test file
    test_contents = "Hello, this is test content!\nLine 2\nLine 3"
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', delete=False) as temp_file:
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
    
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', delete=False) as empty_file:
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

    print("⚡ Testing File Reading -- read_source_file(FileEmpty)")
    test_nickname = "test_unexpected_encoding"

    # We need to create a test file
    wrongly_encoded_contents = "This file has a smart quote: …" # this elipse character is not utf-8
    
    with tempfile.NamedTemporaryFile(mode='w', encoding='windows-1252', delete=False) as wrongly_encoded_file:
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
        test_unexpected_encoding
    ]
    
    passed = 0
    for test in tests:
        if test():
            passed += 1

    emoji_result = choose_emoji(passed, len(tests))

    print(f"\n{emoji_result} {passed}/{len(tests)} tests passed {emoji_result}")

if __name__ == "__main__":
    run_tests()
