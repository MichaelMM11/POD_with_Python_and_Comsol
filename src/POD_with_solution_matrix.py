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

from numpy.linalg import inv

should_np_array_be_completely_displayed(True)
set_number_of_digits_after_period(1)

folder_dir = return_folder_dirs()

filename = 'L_shape__data.txt'
data__dir = folder_dir['data']
data_file = Path(data__dir, filename)


snapshot_matrix = Path(data__dir, "L_shape__data__snapshots.dat")
U = load_snapshot_matrix_from_comsol(snapshot_matrix)
U =U.T
#U = np.array([[0,1,3,0], [-2,3,0,4], [0,0,6,1], [0,0,1,6]])

# console.print(f"[red]U =\n {U}")
C = calculate_covariance_matrix(U)
# console.print(f"[yellow]C =\n {C}")
#TKE = calculate_stored_energy(C)

separator()
eigenvalue, eigenvector = np.linalg.eig(C)
# console.print(f"[cyan]eigenvalue =\n {eigenvalue}")
# console.print(f"[blue]eigenvector =\n {eigenvector}")

separator()
sorted_eigenvalues, sorted_eigenvectors = sort_eigenvalues_eigenvectors(eigenvalue, eigenvector)
# console.print(f"[cyan]sorted_eigenvalues =\n {sorted_eigenvalues}")
# console.print(f"[blue]sorted_eigenvectors =\n {sorted_eigenvectors}")




separator()
energy_ratio = 1
show_save_eigenvalue_energy_data(sorted_eigenvalues, energy_ratio)
diag_lambda = create_reduced_Sigma_matrix(sorted_eigenvalues)
# console.print(f"[magenta]diag_lambda =\n {diag_lambda}")

#@ OK
newC = np.matmul(sorted_eigenvectors,np.matmul(diag_lambda,sorted_eigenvectors.T))
# console.print(f"[green]newC =\n {newC}")
# console.print(f"[blue]C =\n {C}")

#@ OK
Phi_m = inv(eigenvector)
Phi_t = eigenvector.T
# console.print(f"[green]Phi_m =\n {Phi_m}")
# console.print(f"[blue]Phi_t =\n {Phi_t}")
#@ OK
A = np.matmul(U, eigenvector)
# console.print(f"[violet]A =\n {A}")

#@ OK
newU = np.matmul(A, eigenvector.T)
# console.print(f"[green]newU =\n {newU}")
# console.print(f"[blue]U =\n {U}")

# matrices_must_be_numerically_close(U, newU)

#@ OK
for i in range(1,6):
    POD_modes = i
    U_tilde = return_matrix_of_summarized_k_th_reduced_POD(A, eigenvector, POD_modes)


    # matrices_must_be_numerically_close(U_tilde, U)
    #@ OK
    filename = f'reduced_matrix_reduction_{POD_modes}.dat'
    reduced_matrix_reduction_ = Path(folder_dir['data'], filename)
    np.savetxt(reduced_matrix_reduction_, U_tilde.T, delimiter='\t')
