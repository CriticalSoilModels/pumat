import numpy as np
import pandas as pd 

def calc_mean_stress(stress):
    """
    Calc the mean stress
    """
    mean_stress = np.sum(stress[0:3]) / 3.0

    return mean_stress

def calc_q_invariant(stress):
    """
    Calc the q invariant
    """
    # Calc the mean stress
    mean_stress = calc_mean_stress(stress)

    # Store a copy of the stress
    dev_stress = stress.copy()

    # Calc the deviatoric stress vector
    dev_stress[0:3] = dev_stress[0:3] - mean_stress

    # Square all the elements 
    dev_stress = dev_stress**2

    # Double the shear stress terms
    dev_stress[3:6] = 2.0 * dev_stress[3:6]

    # Calc the equivlent stress invariant
    q = np.sqrt(3.0 * np.sum(dev_stress) / 2.0)

    return q

def calc_dev_strain_invariant(strain):
    """
    Calc the deviatoric strain invariant
    """
    if isinstance(strain, pd.Series):
        strain = strain.to_numpy()
    elif not isinstance(strain, np.ndarray):
        raise TypeError("Input must be a pandas Series or a NumPy array")
    
    # Ensure that strain is a 1D array
    if strain.ndim != 1 or not len(strain) == 6:
        raise ValueError("Input array must be 1D with 6 elements")
    
    # Calc ( eps_{yy} - eps_{zz} )^{2}
    first_term = (strain[1] - strain[2])**2

    # Calc (eps_{zz} - eps_{xx})^{2}
    second_term = (strain[2] - strain[0])**2

    # Calc (eps_{xx} - eps_{yy})^{2}
    third_term = (strain[0]- strain[1])**2

    # Calc the shear terms (eps_{yz}^{2} + eps_{zx}^{2} + eps_{xy}^{2})
    shear_term = np.sum(strain[3:6]**2)

    eps_q = 1.0/3.0 * np.sqrt( (2.0 * (first_term + second_term + third_term) + 3.0 * shear_term ) )

    return eps_q

def calc_volumetric_strain_invariant(strain):
    """
    Calc the volumetric strain invariant
    """
    # Get the first three components
    eps_p = np.sum( strain[0:3] )
    return eps_p


if __name__ == "__main__":

    # Make a stress vector
    stress = np.array([1, 2, 3, 4, 5, 6])

    print(f"Mean Stress: {calc_mean_stress(stress)}")
    print(f"q invariant: {calc_q_invariant(stress)}")

    # Make a strain vector
    strain = np.array([1,2, 3, 4, 5, 6])
    print(f"Eps_q: {calc_dev_strain_invariant(strain)}")
    print(f"Eps_p: {calc_volumetric_strain_invariant(strain)}")
