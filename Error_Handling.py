import sys

class SDLangErrors: #mixing variables and classes works correctly
    
    INVALID_ENCODING = "SDL-E001"
    @staticmethod
    def handle_invalid_encoding(file_path, i_didnt):
        error_code = SDLangErrors.INVALID_ENCODING
        print(f"I didn't {i_didnt} because the file \"{file_path}\" didn't have the format I expected : {error_code}")
        sys.exit(error_code) #sys.exit() is "SystemExit".
    
    EMPTY_FILE = "SDL-E002"
    @staticmethod
    def handle_empty_file(file_path, i_didnt):
        error_code = SDLangErrors.EMPTY_FILE #calls the string 
        print(f"I didn't {i_didnt} because the file \"{file_path}\" was empty : {error_code}")
        sys.exit(error_code) #this is actually what exits the program

    INVALID_EXTENSION = "SDL-E003"
    @staticmethod
    def handle_invalid_file_type(file_path, i_didnt, file_extension):
        error_code = SDLangErrors.INVALID_EXTENSION
        if file_extension == "":
            print(f"I didn't {i_didnt} because \"{file_path}\" doesn't have a file type like \".sdlang\", : {error_code}")
        else:
            print(f"I didn't {i_didnt} because \"{file_path}\" is a \"{file_extension}\" file, : {error_code}")
        sys.exit(error_code)
    
    READ_FAILED = "SDL-E400" #generic read error

    PERMISSION_DENIED = "SDL-E403"
    #should implement at some point, but not sure how/when
    
    FILE_NOT_FOUND = "SDL-E404"
    @staticmethod #allow you to call the function without making an object
    def handle_file_not_found(file_path, i_didnt):
        # "i_didnt" is a string to be inserted into the error messate
        error_code = SDLangErrors.FILE_NOT_FOUND
        print(f"I didn't {i_didnt} because I couldn't find the file \"{file_path}\" : {error_code}")
        sys.exit(error_code)
    
    WRITE_FAILED = "SDL-E500" #generic write
