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
filename = 'Data.txt'
data_file = Path(data__dir, filename)



snapshot_matrix = load_snapshot_matrix_from_comsol(data_file)


U, sigma_i, V_star = linalg.svd(snapshot_matrix, full_matrices=True)
# console.print(f"[red]U={U}")
# console.print(f"[blue]sigma_i={sigma_i}")
# console.print(f"[violet]V_star={V_star}")
# console.print(f"[yellow]U__dim={get_dimemsions_from_matrix(U)}")
# console.print(f"[yellow]V_star__dim={get_dimemsions_from_matrix(V_star)}")
#list_eigenval__partial_energy__energy_ratio(sigma_i, 0.9)

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

"""
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
"""




"""
https://stackoverflow.com/questions/42426095/matplotlib-contour-contourf-of-concave-non-gridded-data
https://stackoverflow.com/questions/52457964/how-to-deal-with-the-undesired-triangles-that-form-between-the-edges-of-my-geo
https://stackoverflow.com/questions/74659764/triangulation-plot-python-curved-scattered-data
https://matplotlib.org/2.2.3/gallery/images_contours_and_fields/irregulardatagrid.html
https://stackoverflow.com/questions/3373256/set-colorbar-range-in-matplotlib
"""
q = load_mesh_coordinates_from_comsol(data_file)
#@ - same like "load_snapshot_matrix_from_comsol" but mesh"coordinates are
#@   returned
#@ skipped because proof-of-concept if data can be plotted with expected results

import matplotlib.pyplot as plt
import matplotlib.tri as tri
plt.style.use('classic')
x = q[:,0]
y = q[:,1]
z = snapshot_matrix[:,-1]

fig, ax1 = plt.subplots()
triang = tri.Triangulation(x, y,)
interpolator = tri.LinearTriInterpolator(triang, z)
Xi, Yi = np.meshgrid(x, y)
Zi = interpolator(Xi, Yi)
#print(Zi)

# colourbar and contour
cntr2 = ax1.tricontourf(x, y, z, levels=14, cmap="viridis")
cb = fig.colorbar(cntr2, ax=ax1,)


file_to_save = Path(current__dir, 'dummydata.txt')
np.savetxt(file_to_save,Zi)


# dots and lines (but colour+marker+linewidth has to be given)
ax1.triplot(x, y, 'ko-', lw=1)


#plt.contourf(Xi, Yi, Zi, interpolation="linear")

plt.show()