from lib.general_functions.general_functions import write_line_with_inline_comment
import os
import glob

class DriverModelSetup:

    def __init__(self, folder_path, constitutive_model_name,output_file_name):
        self.constitutive_model_name = constitutive_model_name   # Name of the model
        self.folder_path             = folder_path   
        self.output_file_name        = output_file_name

        self.num_state_params = None
        self.load_list = []             # Allow for multiple loads to be stored
        self.num_loads = 0              # counter to keep track of the number of loads
    def __str__(self):
        """
        prints information about the object when the object is inserted
        into a print statement
        """

        return_string = (f"Constitutive model name: {self.constitutive_model_name}\n"
                         f"Folder path: {self.folder_path}\n"
                         f"Number of stored loads: {self.num_loads}\n"
                         )
        
        return return_string
    
    def clear_folder(self, file_extensions=["inp", "bat", "txt"]):
        """
        Delete all files with the specified file extensions in the folder.
        """
        for ext in file_extensions:
            # Create a pattern to match files with the given extension
            pattern = os.path.join(self.folder_path, f'*.{ext}')
            # Use glob to find all files matching the pattern
            for file_path in glob.glob(pattern):
                try:
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
                except OSError as e:
                    print(f"Error: {file_path} : {e.strerror}")

    def store_loads(self, new_loads):
        """
        Store the load in the setup
        """
        
        # If the load isn't a load object then
        if not isinstance(new_loads, list):
            # Mke the load into a list
            new_load_list = [new_loads]
        else:
            # Already a list
            new_load_list = new_loads

        # Append the load(s) to the list
        self.load_list = self.load_list + new_load_list

        # Store the number of loads
        self.num_loads = len(self.load_list)

    def delete_all_loads(self):
        """
        Deletes the reference to the load object from the DriverSetup object
        """
        self.load_list = []
    
    def write_parameters_file(self, properties, num_spaces = 10,
                               params_file_name = "parameters.inp"):
        """
        Make the parameters.inp file

        Write the name of the state parameters as a comment 
        10 spaces after the input before the comment

        Input: 
            num_spaces: Number of spaces betwe
        """
        
        file_path = os.path.join(self.folder_path, params_file_name)
        
        num_props = len(properties)

        # Get the load name from the load object
        with open(file_path, "w+") as file:
            # Write the model name
            write_line_with_inline_comment(file, self.constitutive_model_name,
                                           "Model name", num_spaces=num_spaces)
            # Write the number of props
            write_line_with_inline_comment(file, num_props, "Number of properties", 
                                           num_spaces = num_spaces)

            # Write the parameters in the order that they were entered in the dict
            for key, val in properties.items():
                write_line_with_inline_comment(file, val, key, 
                                               num_spaces = num_spaces)

    
    def write_initial_conditions_file(self, init_stress, init_state_vars, file_name = "initialconditions.inp",
                                      num_spaces = 15, stress_names = ["s11", "s22", "s33", "s12", "s13", "s23"]):
        """
        Write the initial conditions of the file

        The initial stress is always defined with the Cartesian components

        """        

        # Get the number of stress values
        num_stress_vals = len(init_stress)

        # Get the number of state parameters
        # An empty string evaluates to zero, this might be a common input since the state params are 
        # automatically initialized to zero
        num_state_vars = len(init_state_vars)

        file_path = os.path.join(self.folder_path, file_name)

        with open(file_path, "w+") as file:
            # Write the number of stress components
            write_line_with_inline_comment(file, num_stress_vals, "ntens, tension is positive", num_spaces = num_spaces)

            # Write the stress components
            for i, stress in enumerate(init_stress):
                # Write the stress values and the comment
                write_line_with_inline_comment(file, stress, stress_names[i], num_spaces = num_spaces)

            # If state variables are pased, right the info
            write_line_with_inline_comment(file, num_state_vars, "Number of state variables", num_spaces = num_spaces)

            # Write the state variables
            for key, val in init_state_vars.items():
                # Write the state parameter values
                write_line_with_inline_comment(file, val, f"{key} - init value", num_spaces = num_spaces)


    def write_loads(self, file_name = "test.inp", num_spaces = 10):
        """
        Write the file that contains the load test

        Write the name of the output file here
        """
        if len(self.load_list) == 0:
            raise Warning("No loads stored in the setup.load_list")
        # Make the file path
        file_path = os.path.join(self.folder_path, file_name)

        # Open the file and write the data to the file
        with open(file_path, "w+") as file:

            # Write the name of the output file
            file.write(self.output_file_name + "\n")

            # Loop over the loads and write the data for each load
            for load in self.load_list:
                load.write(file, num_spaces)

            # Write *End at the end of the file
            file.write("*End")

