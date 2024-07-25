import os
import pandas as pd
import numpy as np
from typing import List, Dict, AnyStr
from lib.Driver_Classes.Mod_Driver_Setup import DriverModelSetup
from lib.Driver_Classes.Mod_Driver_Results import DriverModelResults
from lib.general_functions.executing_runs import run_batch_script, generate_batch_script


class DriverModel:
    """
    Model wraps the setup and results classes 
    """
    def __init__(self, folder_path, constitutive_model_name, 
                 inc_driver_exe_path, output_file_name = "output.txt"):
        
        # Init setup object
        self.setup = DriverModelSetup(folder_path, constitutive_model_name, output_file_name)

        # init results object
        self.results = DriverModelResults(folder_path, output_file_name)

        # Store the path to the incremental driver exe
        self.inc_driver_exe_path = inc_driver_exe_path

        # Store the path to the folder containing all of the incremental driver files
        self.folder_path = folder_path

    def __str__(self):
        """
        Prints information object the object when the object is called
        inside of a print() function
        """

        return_string = ("Put something here")

        # Figure out a way to combine the output of the results 
        # and the setup
        return return_string

    def run_model(self):
        """
        Runs the incremental driver test
        """

        batch_file_name = "run_model.bat"
        
        # Generate the batch script
        generate_batch_script(self.folder_path, self.inc_driver_exe_path, batch_file_name=batch_file_name)
        
        batch_file_path = os.path.join(self.folder_path, batch_file_name)

        # Run the model
        run_batch_script(batch_file_path)
        


if __name__ == "__main__":

    pass
