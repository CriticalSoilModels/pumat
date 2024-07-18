"""
General functions
"""

def are_keys_in_list(dictionary, lst):
    print(f"dict keys: {dictionary.keys()}")
    print(f"list: {lst}")
    return list(dictionary.keys()).issubset(lst)

def is_list_in_dict_keys(lst, dictionary):
    # Checks if all the elements of a list in the keys of a dict
    return set(lst).issubset(dictionary.keys())

def write_line_with_inline_comment(file, data, comment, 
                                   comment_char = "#", num_spaces = 10,
                                   newline = True):
    """
    Write a line to a file with a comment.

    Inputs:
        file: The file that the line and comment should be written to
        line_data: The data that goes before the comment
        comment: The string that should go after the comment character
        comment_char: The character that comes before the comment
        spaces: Number of spaces between the line data and the comment
        """
    # Store a space character
    space = " "
    
    blank_spaces = space * num_spaces

    # Concatenate the data and the comment with the required spaces
    if newline:
        file_line = f"{data}{blank_spaces}{comment_char} {comment}\n"
    else:
        file_line = f"{data}{blank_spaces}{comment_char} {comment}"

    file.write(file_line)