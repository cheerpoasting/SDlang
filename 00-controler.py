############################################################################
#                                                                          #
#      Self-Documenting Programming Language with a focus on Business      #
#                                                                          #
# Version Number: 00.00.01-alpha                                           #
#                                                                          #
# Last Updated: 08 AUG 2025                                                #
#                                                                          #
# Program Purpose: This program will open a source file, and write its     #
#   contents directly to an output file, without transforming it in        #
#   any way.                                                               #
#                                                                          #
############################################################################

# TEMPLATE
# Open input file
# Transform contents (later)
# Write Contents to output file

# DATA STRUCTURE AREA.

#Source Variables.
# source_path: str #the file path for the source file
# source_file #textIO, the actual source file
# source_content: str #the textual contents of the file

#Transformation Variables.
# transformed_content: str
# thing_to_be_transformed: str

#Output Variables.
# output_path: str #the file path for the output file
# output_file #textIO, the actual output file
# output_content: str # the textual contents of the output file

# CODE AREA.

def read_source_file(source_path):
    with open(source_path, 'r', encoding='utf-8') as source_file:
        source_content = source_file.read()
        print(f"succesfully read {len(source_content)} characters from {source_path}")
        return source_content

def transform_content(thing_to_be_transformed):
    print("contents would be transformed here in the future")
    return thing_to_be_transformed

def write_output_file(content_to_save, output_path):
    with open(output_path, 'w', encoding='utf-8') as output_file:
        output_file.write(content_to_save)
        print(f"succesfully wrote {len(content_to_save)} characters to {output_path}")


def main():
    print("program ran")
    source_content = read_source_file("file-to-be-parsed.sdlang")
    transformed_content = transform_content(source_content)
    write_output_file(transformed_content, "final-python-file.py")

if __name__ == "__main__":
    main()
