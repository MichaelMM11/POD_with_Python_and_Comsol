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


should_np_array_be_completely_displayed(True)
set_number_of_digits_after_period(1)


current__dir = Path.cwd()
main__dir = current__dir.parents[0]
comsol__dir = main__dir.joinpath('comsol')
data__dir = main__dir.joinpath('data')
src__dir = main__dir.joinpath('src')
filename = 'raw_comsol_data____simplest.txt'
data_file = Path(data__dir, filename)



snapshot_matrix = load_snapshot_matrix_from_comsol(data_file)


U, sigma_i, V_star = linalg.svd(snapshot_matrix, full_matrices=True)
# console.print(f"[red]U={U}")
# console.print(f"[blue]sigma_i={sigma_i}")
# console.print(f"[violet]V_star={V_star}")
# console.print(f"[yellow]U__dim={get_dimemsions_from_matrix(U)}")
# console.print(f"[yellow]V_star__dim={get_dimemsions_from_matrix(V_star)}")
list_eigenval__partial_energy__energy_ratio(sigma_i, 1)

reduced_Sigma = create_reduced_Sigma_matrix(sigma_i)
# console.print(f"[blue]sigma_i={sigma_i}")
# console.print(f"[yellow]sigma_i__**2={np.square(sigma_i)}")
# console.print(f"[red]red_Sigma={reduced_Sigma}")

reduced_matrix = return_reduced_matrix_from__U_S_Vstar(U, reduced_Sigma, V_star, rank=4)
# console.print(f"[magenta]reduced_matrix={reduced_matrix}")
# console.print(f"[blue]sol_matrix={snapshot_matrix}")

# reduced_matrix_filename = 'x.txt'
# file_to_save = Path(current__dir, reduced_matrix_filename)
# np.savetxt(file_to_save,data)

# print((snapshot_matrix))
# print((reduced_matrix))
