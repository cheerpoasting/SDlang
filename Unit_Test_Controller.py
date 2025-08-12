import os
import tempfile

from Main_Controller import *

# Initial File Opening
def test_initial_file_reading():

    print("⚡ Testing File Reading -- read_source_file(Correct_Filepath)")
    
    # First, create a temportay test file
    test_contents = "Hello, this is test content!\nLine 2\nLine 3"
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', delete=False) as temp_file:
        temp_file.write(test_contents)
        temp_file_path = temp_file.name

    # Test the function here
    try: 
        result = read_source_file(temp_file_path)
        if result == test_contents:
            print("✅ test_read_file PASSED\n")
            return True
        else:
            print(f"💩 test_read_file FAILED: content doesn't match")
            print(f"Expected: {test_content}")
            print(f"Got: {result}\n")
            return False

    # Get rid of the temporary file
    finally:
        os.unlink(temp_file_path)

def test_reading_nonexistent_file():

    print("⚡ Testing File Reading -- read_source_file(FileNotFound)")
    
    # We don't need to make a file, because the point is not to find one
    fake_path = "nonexistant_file.txt"

    try:
        result = read_source_file(fake_path)
        print("💩 test_reading_nonexistent_file FAILED: should have exited\n.")
        return False
    except SystemExit as e:
        # Check if it exited with the right error code
        if str(e) == "SDL-E404":
            print("✅ test_reading_nonexistent_file PASSED: correctly exited with SDL-E404")
            return True
        else:
            print(f"💩 test_reading_nonexistent_file FAILED: wrong exit code: {e}")
            return False
    except Exception as e:
        print(f"💩 test_read_nonexistent_file FAILED: unexpected error: {e}")
        return False

def choose_emoji(tests_passed, tests_run):
    emoji_result = (tests_passed/tests_run)
    if emoji_result == 1:
        return "🎁"
    elif emoji_result < 0.5:
        return "💩"
    else:
        return "😭"        
    

def run_tests():
    tests = [
        test_initial_file_reading,
        test_reading_nonexistent_file
    ]
    
    passed = 0
    for test in tests:
        if test():
            passed += 1

    emoji_result = choose_emoji(passed, len(tests))

    print(f"\n{emoji_result} {passed}/{len(tests)} tests passed {emoji_result}")

if __name__ == "__main__":
    run_tests()
