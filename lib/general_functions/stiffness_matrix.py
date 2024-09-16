"""
Form the stiffness matrix and other stuff like that
"""

# Standard imports
import numpy as np


def form_stiffness_matrix(G, nu):
    """
    Purpose: 
    Forms the stiffness matrix using the shear modulus (G) and poisson's ratio
    
    """

    # Init the matrix with zeros
    stiff_matrix = np.zeros([6, 6])

    # Calc the terms needed for the matrix
    term_1 = 2 * G * ( 1- nu ) / (1 - 2 * nu)
    term_2 = 2 * G * nu  / (1 - 2 * nu)

    # Fill the upper left block
    stiff_matrix[0:3, 0:3] = term_2

    # Fix the diagonal
    for i in range(4):
        stiff_matrix[i, i] = term_1
    
    for i in range(3, 6): 
        stiff_matrix[i, i] = G

    return stiff_matrix
