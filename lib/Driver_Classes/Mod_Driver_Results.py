# Standard imports
import os
import pandas as pd
import matplotlib.pyplot as plt

# Lib imports
from lib.general_functions.invariant_functions import (
     calc_mean_stress, calc_q_invariant, calc_dev_strain_invariant, calc_volumetric_strain_invariant
)

class DriverModelResults:
    """
    Class to represent the results of the driver model
    """

    def __init__(self, results_folder_path, output_file_name = "output.txt"):
        # Store the folder that the results are in
        self.results_folder_path = results_folder_path

        # Store the name of the output file
        self.output_file_name = output_file_name

        # Construct the file path
        self.output_file_path = os.path.join(results_folder_path, output_file_name)

        # variable to store the output file df
        self.output_df = None

        # Variables to hold the results from the incremental driver run
        self.time          = None
        self.stress_df     = None
        self.strain_df     = None
        self.state_vars_df = None

    def __str__(self) -> str:
        return_string = (f"Output file name: {self.output_file_name}\n"
                         f"Results folder path: {self.results_folder_path}\n"
        )

        return return_string

    def get_output_file_as_df(self):
        """
        Return the output file as a df
        """

        # Read the file as a df, delim using white space
        df = pd.read_csv(self.output_file_path, sep = '\\s+')

        return df

    def store_output_file_as_df(self):
        """
        Read the output file
        """
        df = self.get_output_file_as_df()

        # Store the df
        self.output_df = df

    def store_times(self,
                    col_names = ["time(1)", "time(2)"]):
        """
        Store the times
        TODO: Don't know the difference between time1 and 2
        """

        if self.output_df is None:
            df = self.get_output_file_as_df()
        else:
            df = self.output_df

        self.time_df = df[col_names]
 
    def store_output_stress(self, 
                           col_names = ["stress(1)", "stress(2)", "stress(3)", 
                                        "stress(4)", "stress(5)", "stress(6)"]):
        """
        Store the stress terms
        """

        if self.output_df is None:
            df = self.get_output_file_as_df()
        else:
            # df already stored
            df = self.output_df

        self.stress_df = df[col_names]

    def store_output_strains(self,
                             col_names = ["stran(1)", "stran(2)", "stran(3)",
                                          "stran(4)", "stran(5)", "stran(6)"]):
        if self.output_df is None:
            df = self.get_output_file_as_df()
        else:
            df = self.output_df

        self.strain_df = df[col_names]

    def store_output_state_vars(self, substring = "statev"):
        """
        Gets the state variables from the output.txt file
        """

        if self.output_df is None:
            df = self.get_output_file_as_df()
        else:
            df = self.output_df
        
        # Get the column names that have statv in them
        # The number of them depends on the model
        # Incremental driver always outputs at least one even if zero are passed
        # TODO: look into this
        col_names = [name for name in df.columns if "statev" in name]

        self.state_vars_df = df[col_names]

    def store_all(self):
        """
        Store the df and each of the variables
        """
        self.store_output_file_as_df()

        # Store the stress variables
        self.store_output_stress()
        
        # Store the strain variables
        self.store_output_strains()

        # Store the state variables
        self.store_output_state_vars()

    def get_mean_stress(self):
        """
        Returns the mean stress applied to a df
        """

        mean_stress = self.stress_df.apply(calc_mean_stress, axis = 1)

        return mean_stress
    
    def get_q_invariant(self):
        """
        Returns the deviatoric stress invariant
        """

        q = self.stress_df.apply(calc_q_invariant, axis = 1)

        return q

    def get_volumetric_strain(self):
        """
        Returns the volumetric strain using the strain df
        """
        eps_p = self.strain_df.apply(calc_volumetric_strain_invariant, axis = 1)

        return eps_p
    
    def get_deviatoric_strain(self):
        """
        Returns the deviatoric strain
        """
        eps_q = self.strain_df.apply(lambda row: calc_dev_strain_invariant(row), axis = 1)

        return eps_q
    
    def quick_plot_stress(self, figsize = (8, 4), compression_pos = True, axs = None, **kwargs):
        """
        Make the q vs. p plot
        """

        # Assumes that the stress variables are already loaded
        # Make the figure if no axs object is passed
        if axs is None:
            fig, axs = plt.subplots(nrows = 1, ncols = 1, figsize = figsize)
        
        # Check if compression should be positive
        if compression_pos:
            sign = -1.0
        else:
            sign = 1.0

        # Calc the q invariant
        mean_stress = sign * self.get_mean_stress()
        q           = self.get_q_invariant()

        axs.plot(mean_stress, q, **kwargs)

        # Format the plot
        axs.set_title("Deviatoric Stress vs. Mean Stress")
        axs.set_xlabel("Mean Stress")
        axs.set_ylabel("Deviatoric Stress")

    def quick_plot_strain(self, figsize = (8, 4), compression_pos = True, axs = None, **kwargs):
        """
        Make the $eps_q$ vs. $eps_v$ plot
        """

        # Check if compression should be positive
        if compression_pos:
            sign = -1.0
        else:
            sign = 1.0

        if axs is None:
            fig, axs = plt.subplots(nrows = 1, ncols = 1, figsize = figsize)
        
        eps_p = sign * self.get_volumetric_strain()
        eps_q = self.get_deviatoric_strain()

        axs.plot(eps_p, eps_q, **kwargs)

        axs.set_title(r"$\epsilon_{q}$ vs. $\epsilon_{p}$ invariants")
        axs.set_xlabel(r"Volumetric strain invariant, $\epsilon_{p}$")
        axs.set_ylabel(r"Deviatoric strain invar, $\epsilon_{q}$")

    def quick_quad_plot(self, figsize = (10,10), axial_strain_id = "stran(1)",
                        stress_units = "kPa", strain_units = "-",
                        compression_pos = True):
        """
        Make the quad plot that is really helpful for visualizing soil
        """

        # Make the figure and axs
        fig, axs = plt.subplots(nrows = 2, ncols = 2, figsize = figsize)

        if compression_pos:
            # flip the sign of the values
            sign = -1.0
        else:
            sign = 1.0

        # Get the data
        axial_strain = sign * self.strain_df[axial_strain_id]
        mean_stress  = sign * self.get_mean_stress()
        q            = self.get_q_invariant()
        vol_strain   = sign * self.get_volumetric_strain()


        # Make the q vs. axial strain \epsilon_{a}
        axs[0, 0].plot(axial_strain, q)

        # Format plot
        axs[0,0].set_title(r"q vs. $\epsilon_{a}$")
        axs[0,0].set_xlabel(r"$\epsilon_{a}$ " + f"[{strain_units}]")
        axs[0,0].set_ylabel(f"q [{stress_units}]")

        # Make the q vs. p plot
        axs[0, 1].plot(mean_stress, q)

        # Format the plot
        axs[0, 1].set_title(r"q vs. p")
        axs[0, 1].set_xlabel(f"p [{stress_units}]")
        axs[0, 1].set_ylabel(f"q [{stress_units}]")

        # Make the \epislon_{v} vs \epsilon_{a} plot
        axs[1, 0].plot(axial_strain, vol_strain)
        
        # Format the plot
        axs[1, 0].set_title(r"$\epsilon_{v}$ vs. $\epsilon_{a}$")
        axs[1, 0].set_xlabel(r"$\epsilon_{a}$" +  f"[{strain_units}]")
        axs[1, 0].set_ylabel(r"$\epsilon_{v}$" +  f"[{strain_units}]")

        # Make the \episilon_{v} vs. p plot
        axs[1, 1].plot(mean_stress, vol_strain)

        # Format the plots
        axs[1, 1].set_title(r"$\epsilon_{v}$ vs. p")
        axs[1, 1].set_xlabel(f"p [{stress_units}]")
        axs[1, 1].set_ylabel(r"$\epsilon_{v}$" +  f"[{strain_units}]")

        # Help make the plots not overlap
        plt.tight_layout()


