#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
purpose
    - 

remark
    - 
"""

import numpy as np
from pathlib import Path
from numpy.linalg import eig


current__dir = Path.cwd()
main__dir = current__dir.parents[0]
comsol__dir = main__dir.joinpath('comsol')

sol_matrix_filename = 'Data.txt'

file_to_load = Path(comsol__dir, sol_matrix_filename)



def data_must_have_float_entries(data):
    to_check = np.isnan(data)
    if True in to_check:
        error_msg = 'Error: data corrupt'
        display_tailored_error_message(error_msg)



def print_dimemsions_from_matrix(matrix):
    rows, columns = np.shape(matrix)[0], np.shape(matrix)[1]
    print(f"number of rows:    {rows}\nnumber of columns: {columns}")

sol_matrix = np.genfromtxt(file_to_load, comments='%')

                        #delimiter='\t', dtype=float, skip_header=1,)






sol_matrix_transpose = np.matrix.transpose(sol_matrix)







covariant_matrix = np.matmul(sol_matrix_transpose, sol_matrix)


eigenvalues, eigenvectors = eig(covariant_matrix)
#print(eigenvalues)
#print(eigenvectors)




def list_eigenval__partial_energy__energy_ratio(eigenvalues):
    number_of_eigenvalues = len(eigenvalues)
    total_energy = np.sum(eigenvalues)
    partial_energy = 0

    for i in range(number_of_eigenvalues):
        ith_eigenvalue = i
        partial_energy += eigenvalues[ith_eigenvalue]
        energy_ratio = partial_energy/total_energy
        print(f"{i}  {eigenvalues[i]}     {partial_energy}      {energy_ratio}")

#list_eigenval__partial_energy__energy_ratio(eigenvalues)


def reduced_matrix(number, eigenvalues, eivenvectors):
    reduced_eigenvalues = eigenvalues[:number]
    reduced_eigenvectors = eivenvectors[:,number]
    return reduced_eigenvalues, reduced_eigenvectors
#     a = np.matrix()

a, b = reduced_matrix(3, eigenvalues, eigenvectors)

#print(a)
#print(b)
#print(eigenvectors[:,:])

def fast_check(w, v, a):
    # https://scriptverse.academy/tutorials/python-eigenvalues-eigenvectors.html
    for i in range(len(a)):
        print(np.allclose(np.dot(a,v[:,i]),np.dot(w[i],v[:,i])))

a = np.array([[3, 1], 
              [2, 2]])
w, v = np.linalg.eig(a)
print(w)
print(v)
fast_check(w, v, a)

fast_check(eigenvalues, eigenvectors, covariant_matrix)

exit()
a = np.array([[3, 1], 
              [2, 2]])
w, v = np.linalg.eig(a)

w, v, a = eigenvalues, eigenvectors, covariant_matrix
print(np.allclose(np.dot(a,v[:,3]),np.dot(w[3],v[:,3])))
print(a)
print()
print(w[:2])
#print(w)
print()
#print(v[:,1-2])
#print(v)



