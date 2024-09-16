#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
purpose
    - this file calculates the difference matrix of the original snapshot
        matrix and the reduced order matrices
    - for convenience regex is used to read all reduced order matrices
        (because these matrices are generated on the fly postprocessing is no
        issue)
    - output is simple matrix/values, no connection to geometry/mesh
"""

from convenience import *
import numpy as np
from pathlib import Path

folder_dir = return_folder_dirs()
data__dir = folder_dir['data']
data_modes_dir = folder_dir['data_modes']
snapshot_file = 'from_Comsol_odd_timesteps__snapshots.dat'

snapshot_matrix = Path(data__dir, snapshot_file)
U = load_snapshot_matrix_from_comsol(snapshot_matrix)

pathlist = sorted(Path(data_modes_dir).rglob('reduced_matrix_of_*'))
# @ - should be in regex form, it's in your interest to be generic

counter = 0
for path in pathlist:
    counter += 1
    path_in_str = str(path)
    reduced_matrix = load_snapshot_matrix_from_comsol(path_in_str)
    differene_matrix = U - reduced_matrix
    filename = f'difference_snapshot_and_{counter}modes_reduction_matrix.dat'
    reduced_matrix_reduction_ = Path(data_modes_dir, filename)
    np.savetxt(
        reduced_matrix_reduction_,
        differene_matrix,
        delimiter='\t')
