def make_file(folder_path, file_name, setting = "w+"):
    """
    Make a file, return the file object and set the mode for the file
    """
    
    file_path = os.path.join(folder_path, file_name)
    file = open(file_path, setting)
    return file

def write_list_2_file(data_list, folder_path, file_name, write_setting, close_file = True, file_obj = None):
    """
    Write the parameters for a soil model
    """
    if file_obj is None:
        # Make the file
        file = make_file(folder_path, file_name, setting = write_setting)
    for val in data_list:
        file.write(f"{val}\n")
    # If the function should close the file close the file
    if close_file:
        file.close()
            
def write_params_file(param_dict, folder_path, file_name = "parameters.inp"):
    """
    Write the parameters file for the incremental driver model
    """
    # Get all of the values from the param dict
    list_vals = param_dict.values()
    file_path = os.path.join(folder_path, file_name)
    # Make the file
    write_file = "w+"
    file = open(file_path, write_file)
    write_list_2_file(list_vals, folder_path, file_name, write_setting= "a", close_file=True, file_obj=file)