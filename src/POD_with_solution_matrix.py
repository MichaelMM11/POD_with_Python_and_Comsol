#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
purpose
    - return reduced matrix from Comsol solution matrix

remark
    - SVD and POD
"""

# try:
#     import sys
#     sys.path.append('~/Desktop/x')
#     from convenience import *
#         # console, \
#         # separator \
#         # my_timer, \
#         # perf_counter, \
#         # show_abs_rel_error, \
#         # convert_to_scientific_notation
# except Exception as e:
#     log.warning(e)

from convenience import *

import numpy as np
from pathlib import Path
from scipy import linalg


should_array_be_completely_displayed = False
if should_array_be_completely_displayed:
    np.set_printoptions(threshold=np.inf)


current__dir = Path.cwd()
main__dir = current__dir.parents[0]
comsol__dir = main__dir.joinpath('comsol')
solution_matrix_filename = 'Data.txt'
file_to_load = Path(comsol__dir, solution_matrix_filename)


solution_matrix = np.genfromtxt(file_to_load, comments='%')
#list_eigenval__partial_energy__energy_ratio(eigenvalues, )




# solution_matrix = np.array([[2, -2, -2/3], [2/3, 2, -2], [2/5, 2/3, 2]])

U, sigma_i, V_star = linalg.svd(solution_matrix, full_matrices=True)
# console.print(f"[red]U={U}")
# console.print(f"[blue]sigma_i={sigma_i}")
# console.print(f"[violet]V_star={V_star}")
# console.print(f"[yellow]U__dim={get_dimemsions_from_matrix(U)}")
# console.print(f"[yellow]V_star__dim={get_dimemsions_from_matrix(V_star)}")


reduced_Sigma = create_reduced_Sigma_matrix(sigma_i)
# console.print(f"[blue]sigma_i={sigma_i}")
# console.print(f"[yellow]sigma_i__**2={np.square(sigma_i)}")
# console.print(f"[red]red_Sigma={reduced_Sigma}")


reduced_matrix = return_reduced_matrix_from__U_S_Vstar(U, reduced_Sigma, V_star, rank=13)
console.print(f"[magenta]reduced_matrix={reduced_matrix}")
console.print(f"[blue]sol_matrix={solution_matrix}")





#! just sandbox for trial & error
# - https://modred.readthedocs.io/en/stable/tutorial_modaldecomp.html
# import numpy as np
# import modred as mr
# # Compute POD
# num_modes = 2
# solution_matrix = np.array([[2, -2, -2/3], [2/3, 2, -2], [2/5, 2/3, 2]])
# POD_res = mr.compute_POD_arrays_snaps_method(
#     solution_matrix, list(mr.range(num_modes)))
# modes = POD_res.modes
# eigvals = POD_res.eigvals
# console.print(f"[red]{modes}")
# console.print(f"[blue]{eigvals}")


# from scipy.linalg import svdvals
# sigma_i = svdvals(solution_matrix)
# console.print(f"[blue]{sigma_i}")
