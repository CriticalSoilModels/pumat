from pyIncrementalDriver.python_files.lib.general_functions import write_line_with_inline_comment, is_list_in_dict_keys

#TODO: Generate an abstract class that can serve as the base class for all the load types and use that to generate all of the load types

class PopularPath:
    """
    Class that represents the popular paths available in 
    incremental driver
    """
    # Common values required by all the popular paths
    common_vals = ["ninc", "maxiter", "dtime", "every"] 

    def __init__(self, test_name, input_params_dict) -> None:
        
        # Check that the test name and the input params are valid  
        self.test_name, self.input_params_dict = self._check_inputs(test_name, input_params_dict)

        # Set values for later use
        self.predifined_cond = None # Used to store the predifined condition if there is one

    def __str__(self) -> str:
        return_string = (
            f"Test Name: {self.test_name}\n"
            f"Load Properties: {self.input_params_dict}"
        )

        return return_string
    @staticmethod
    def _check_inputs(test_name, input_params_dict):
        """
        Check that the input information mets the minimum requirements for the popular path
        """

        oedo = "Oedometric"
        trx = "Triaxial"
        pure_relaxation = "PureRelaxation"
        pure_creep = "PureCreep"
        undrained_creep = "UndrainedCreep"
        
        # Dict of the popular paths and the required params
        allowed_popular_paths = {
            oedo + "E1" : PopularPath.common_vals + ["ddstran_1" ], # lateral strain is assumed constant
            oedo + "S1" : PopularPath.common_vals + ["ddstress_1"], # lateral strain is assumed constant
            trx  + "E1" : PopularPath.common_vals + ["ddstran_1" ], # lateral stress is assumed constant
            trx  + "S1" : PopularPath.common_vals + ["ddstress_1"], # lateral stress is assumed constant
            trx  + "UEq": PopularPath.common_vals + ["ddstran_2" ], # volume = const., Roscoe's Delta epsilon_q is applied
            trx  + "Uq" : PopularPath.common_vals + ["ddstress_2"], # volume = const., Roscoe's Delta q is applied
            pure_relaxation : PopularPath.common_vals,
            pure_creep      : PopularPath.common_vals,
            undrained_creep : PopularPath.common_vals,
        }
        
        # Check that the input test name is one of the allowed
        if test_name in allowed_popular_paths:
            # Get the required params  
            required_params_list = allowed_popular_paths[test_name]
        else:
            # raise an error saying that the test isn't one
            raise ValueError(f"{test_name} is not one of the allowed test."
                           f"The allowed tests are: {allowed_popular_paths.keys()}"
                           )
        
        # Check that all of input params are in the required params
        if not is_list_in_dict_keys(required_params_list, input_params_dict):
            
            # If the keys aren't in the list throw an error
            input_keys = input_params_dict.keys()
            
            error = (f"The selected test is: {test_name}\n"
                    f"The input keys are: {input_keys}\n"
                    f"The required params are: {required_params_list}")
            raise ValueError(error)
        
        # If the values make it this far, they are valid inputs return them
        return test_name, input_params_dict


    def set_predifined_condition(self, left_side_eqn, right_side_value, less_than = True,
                                 parsing_symbol = "?"):
        """
        Set a predined condition using one of the stress or strain parameters

        Inputs:
            left_side_eqn: Equation on the left side of the inequality that defines the value constrained and operations on it
            right_side_value: Value on the right hand side of the inequality that is the constraint.
            less_than (bool) : Logical that determines if the sign should be less than or greater than
        """
        #TODO: Add a check that the inputs meet the specifications of incremental driver

        #--- Construct the equation ---

        # Make the inequality sign
        if less_than:
            inequality = " < "
        else:
            inequality = " > "

        # Add a space before and after the parsing symbol
        parsing_with_space = f" {parsing_symbol} "

        # Make the full statement
        condition_str = parsing_with_space + left_side_eqn + inequality + right_side_value

        # Store the predifined condition in the object
        self.predifined_cond = condition_str


    def write(self, file, num_spaces = 10):
        """
        Write the load to a file. This module assumes that the data should be written in 
        append mode
        
        Inputs:
            file: File object that the data should be written in
            write_mode (str): Mode that writing should be done in the file. "a" means that the data should be appended to the file
        """

        # if None there is no predifined condition to set
        if not self.predifined_cond is None:
            # Otherwise construct the load header
            header = "*" + self.test_name  + self.predifined_cond + "\n"
        else:
            header = "*" + self.test_name + "\n"

        # Init load key to None so that it can be filled later if there is a load supplied
        load_key = None

        # Check if the stress or strain load is required and store the name of the stress or strain key
        for key in self.input_params_dict.keys():
            if "ddstress_" in key or "ddstran_" in key:
                load_key = key

        # Write the header of the load
        file.write(header)
        
        
        ninc = self.input_params_dict["ninc"]
        maxiter = self.input_params_dict["maxiter"]
        dtime = self.input_params_dict["dtime"]
        every = self.input_params_dict["every"]

        comment = "ninc maxiter dtime : every"
        general_info = f"{ninc} {maxiter} {dtime} : {every}"

        # Write the general information 
        write_line_with_inline_comment(file, general_info, comment,
                                        comment_char= "#", num_spaces =num_spaces)
        
        if not load_key is None:
            # Write the stress condtion
            write_line_with_inline_comment(file, self.input_params_dict[load_key], load_key,
                                           comment_char="#", num_spaces = num_spaces)
