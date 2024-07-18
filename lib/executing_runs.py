import os
import subprocess

def generate_batch_script(model_folder, exe_path, batch_file_name = "run_model.bat", include_cd = False, batch_file_folder = None):
    """
    Generates an batch script inside of the model directory, linking to the exe_path
    
    Parameters
    ----------
    model_folder: string
        Directory to the model that the batch script should be created for
    
    exe_path: string
        Directory to the executable that should be linked to in the batch file
    
    batch_file_name: string (Optional)
        Name of the batch script that should be generated. Defaults to "run_model.bat"
    
    include_cd: Boolean (Optional)
        Controls if a "cd {model directory}" statement is included in the batch file.

    batch_file_folder: string (Optional)
        Input a directory that should hold the batch file. This overrides including the file inside of the model folder
        NOTE: This causes include_cd to be True
    Returns
    -------
    None.
    
    """

    if batch_file_folder is None:
        # Make the batch file path
        batch_script_path = os.path.join(model_folder, batch_file_name)
    
    else:
        # Make the include_cd statement true, because for the batch file to be saved in a different directory than the model it will have to cd into
        # that directory
        include_cd = True
        batch_script_path = os.path.join(batch_file_folder)

    # init empty string to possibly hold the change directory statement
    cd_str = ""

    if include_cd:
        cd_str = "cd \"{}\"".format(model_folder)

    # Make the string that will be written to the file
    batch_str = cd_str + "call \"{}\"".format(exe_path)

    # Create the file and open it in write mode
    with open(batch_script_path, "w") as f:
        # write the string to the batch file
        f.write(batch_str)

def run_batch_script(batch_script_path, flag_print_Blog = False):
    """
    Run a batch script given a path
    
    Parameters
    ----------
    batch_script_path : string
        The path to a batch script that the user wants to run. This will cause the script to be run inside of the python script

    Returns
    -------
    None.

    '''
    """

    # Set the working directory to where the batch file is located
    working_directory = os.path.dirname(batch_script_path)

    try:
        # Execute the batch file, capturing both stdout and stderr
        result = subprocess.run(batch_script_path, check=True, shell=True, cwd=working_directory, capture_output=True, text=True)
        
        # Print success message and output
        print(f"Batch file '{batch_script_path}' executed successfully.")

        if flag_print_Blog:
            print("Output:")
            print(result.stdout)
    except subprocess.CalledProcessError as e:
        # Print error message and captured stderr
        print(f"An error occurred while executing the batch file: {e}")
        print("Error output:")
        print(e.stderr)