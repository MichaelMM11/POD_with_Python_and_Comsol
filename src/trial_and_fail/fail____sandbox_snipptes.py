
"""
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


########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################


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
