#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
purpose
    - return reduced matrix from Comsol data matrix

remark
    - calculate the impact of the eigenvalues/-vectors for given snapshot
      matrix
    - can be done either by POD or SVD but it's done here with POD
#@ - dummy data for reference if code is doing what is expected to do
#@ - https://www.intmath.com/matrices-determinants/eigenvalues-eigenvectors-calculator.php
M = np.array([[0,1,3,0], [-2,3,0,4], [0,0,6,1], [0,0,1,6]])
# M =>
    # [ 0,  1,  3,  0],
    # [-2,  3,  0,  4],
    # [ 0,  0,  6,  1],
    # [ 0,  0,  1,  6]
# EVal_1=2 => EVec_1:  0.44721,  0.89443,  0,  0
# EVal_2=1 => EVec_2:  0.70711,  0.70711,  0,  0
# EVal_3=7 => EVec_3:   0.5333,   0.7333,  1,  1
# EVal_4=5 => EVec_4: -0.16667,  2.16667, -1,  1
# covariance => 1/3 *
    # [  4  -6   0  -8],
    # [ -6  10   3  12],
    # [  0   3  46  12],
    # [ -8  12   7  23]
    """

from convenience import *

import numpy as np
from pathlib import Path


# should_np_array_be_completely_displayed(True)
# set_number_of_digits_after_period(6)

folder_dir = return_folder_dirs()

filename = 'raw_comsol_data____simplest.txt'
data__dir = folder_dir['data']
data_file = Path(data__dir, filename)


# snapshot_matrix = Path(data__dir, "snapshot_matrix____raw_data.txt")
# U = load_snapshot_matrix_from_comsol(snapshot_matrix)

U = np.array([[0,1,3,0], [-2,3,0,4], [0,0,6,1], [0,0,1,6]])

C = calculate_covariance_matrix(U)

TKE = calculate_stored_energy(C)

lambdas, Phis = np.linalg.eig(U)  #@ M for debugging, but must be C

sorted_eigenvalues, sorted_eigenvectors = sort_eigenvalues_eigenvectors(lambdas, Phis)


show_save_eigenvalue_energy_data(sorted_eigenvalues, 0.9)

diag_lambda = create_reduced_Sigma_matrix(sorted_eigenvalues)


X = np.matmul(Phis, np.matmul(diag_lambda, Phis.T))
console.print(f'[red]X = \n {X}')

console.print(f'[red]C = \n {C}')
exit()
A = np.matmul(U, sorted_eigenvectors)

X = np.matmul(A,sorted_eigenvectors.T)
console.print(f"[green]A =\n {X}")


# def k_th_U_matrix(k, Q, W):
#     """
#     - returns the k_th contribution of the k_th eigenvalue/-vector
#     """
#     pass



# def return_matrix_of_summarized_k_th_reduced_POD(number_of_PODs):
# #@ - eq 25 suggests that for 1 POD first column of A multiplied with first row
# #@   vector of PHI, so col x row => matrix [contribution of 1st mode]
# #@ - same for second mode, 2nd col of A times 2nd row of PHI => this contibution
# #@   of 2nd mode
# #@ - adding first contribution and second contribution results in POD of order 2
# #@   and so on...goes iteratively
#     for i in range(number_of_PODs):
#         pass




exit()
# snapshot_matrix = Path(data__dir, "snapshot_matrix____raw_data.txt")
# U = load_snapshot_matrix_from_comsol(snapshot_matrix)

# snap_rows, snap_cols = get_dimemsions_from_matrix(U)
# snap_transpose = np.matrix.transpose(U)

# covariant_matrix = 1/(snap_rows-1)*np.matmul(snap_transpose, U)

# TKE = 1/(2*(snap_rows-1))*np.matrix.trace(covariant_matrix)

# LAMBDA, PHI = np.linalg.eig(covariant_matrix)  #! not sorted
# #@ - sort eigenvalues and eigenvectors form high to low and the eigenvector 
# #@   matrix
# idx = LAMBDA.argsort()[::-1]
# eigenValues = LAMBDA[idx]
# eigenVectors = PHI[:,idx]
# list_eigenval__partial_energy__energy_ratio(eigenValues)

# diag_lambda = create_reduced_Sigma_matrix(eigenValues)


# eigenVectors_transpose = np.matrix.transpose(eigenVectors)

# A = np.matmul(U, eigenVectors)
# also_U = np.matmul(A, PHI.T)











