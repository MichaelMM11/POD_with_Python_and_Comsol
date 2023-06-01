#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
purpose
    - 

remark
    - 
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
from numpy.linalg import eig



should_array_be_completely_displayed = False
if should_array_be_completely_displayed:
    np.set_printoptions(threshold=np.inf)




current__dir = Path.cwd()
main__dir = current__dir.parents[0]
comsol__dir = main__dir.joinpath('comsol')

solution_matrix_filename = 'Data.txt'

file_to_load = Path(comsol__dir, solution_matrix_filename)









solution_matrix = np.genfromtxt(file_to_load, comments='%')
covariance_matrix = calculate_covariance_matrix(solution_matrix)


eigenvalues, eigenvectors = eig(covariance_matrix)


list_eigenval__partial_energy__energy_ratio(eigenvalues, )

console.print(f"[red]{covariance_matrix}")
console.print(f"[blue]{return_nth_eigenvalue_eigenvector(1, eigenvalues, eigenvectors)}")
console.print(f"[yellow]{create_nth_reduced_diag_eigenvalue_matrix(3, eigenvalues)}")
console.print(f"[violet]{create_nth_reduced_matrix(3,covariance_matrix)}")


#@ can make more dynamic, ie depending on threshold this number is returned \
#  as value and the reduced matrices are generated on the fly




#check_eigenvalue_eigenvector_with_matrix(eigenvalues, eigenvectors, covariant_matrix)


# https://scriptverse.academy/tutorials/python-eigenvalues-eigenvectors.html
# https://pythonnumericalmethods.berkeley.edu/notebooks/chapter15.04-Eigenvalues-and-Eigenvectors-in-Python.html
