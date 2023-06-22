#!/usr/bin/env python3
# -*- coding:utf-8 -*-


"""
purpose
    - provides all kind of functions
      - functions for debugging
      - functions that do the actual computation

remark
    - not sorted but maybe there is need one day to split into semantic files
"""

""" imports
- almost any of these imports is needed in almost any function
"""
import numpy as np
import pandas as pd
from tabulate import tabulate


"""
- creates file where information during runtime is tracked
- can be used to track code smells effectively (because comments are not enough)
- https://docs.python.org/3/howto/logging.html
- https://pyzone.dev/python-logging-module-deep-tutorial/
- options/possible calls:
    - log.info("should be info")
    - log.error("should be error")
    - try:
        1/1
        log.info("fine")
    except:
        log.exception("should only be used in try/except blocks")
    - log.warning("should be warning")
    - log.debug("should be debug")
    - log.critical("should be critical")
"""
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s :: '
           '[%(levelname)-8s] :: '
           '%(lineno)7s :: '
           '%(message)s :: '
           '%(funcName)s',
    filemode='w',
    filename='loggings.log',
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger("my_code")


"""console and print
  - makes developing process easier because of colour
  - options/possible calls:
    - console.print("[blue] Hello World.")
    - console.log("[red]Hello, World.")
    - console.rule(
        title="[red] message",
        characters="-",
        style='gray',
        align="left",
        )
"""
from rich.console import Console
console = Console(highlight=False)


def separator(msg):
    """makes visible line in shell for convenience"""
    text = f"[yellow]↓ {msg} ↓"
    console.print()
    console.print()
    console.rule(title=text, style="black")


"""
  - when execution time of function calls are of interest, this wrapper is
    most useful
"""
from time import perf_counter
def my_timer(func):
    """wrapper to measure evaluation time of functions"""
    def wrapper(*args, **kwargs):
        start = perf_counter()
        result = func(*args, **kwargs)
        end = perf_counter()
        elapsed = end - start
        elapsed = convert_to_scientific_notation(elapsed, 10)
        console.print(f"[blue]Wrapper computation time: {elapsed} s")
        return result
    return wrapper


def inspect(x):
    """returns quick&dirty main information of variable"""
    print(type(x))
    print(x)


def convert_to_scientific_notation(number, digits=10):
    """
    - https://stackoverflow.com/questions/6913532/display-a-decimal-in-scientific-notation
    - https://en.wikipedia.org/wiki/Scientific_notation
    - convenient way to display number with wanted digits after the period
    """
    return f"{number:+.{digits}e}"


def convert_to_float_notation(number, digits=10):
    """
    convenient way to display number with wanted digits after the period
    """
    return f"{number:+.{digits}f}"


def show_abs_rel_error(num_a, num_b):
    abs_err = abs(num_a - num_b)
    rel_err = abs(num_a / num_b)*100
    abs_err = convert_to_scientific_notation(abs_err)
    rel_err = convert_to_float_notation(rel_err)
    console.print(f"[yellow] Absolute error: {abs_err}")
    console.print(f"[yellow] Relative error: {rel_err} %")


def print_dimemsions_from_matrix(matrix):
    """returns quick information of matrix dimensions"""
    rows, columns = get_dimemsions_from_matrix(matrix)
    print(f"number of rows:    {rows}\nnumber of columns: {columns}")


def get_dimemsions_from_matrix(matrix):
    rows, columns = np.shape(matrix)[0], np.shape(matrix)[1]
    return rows, columns


def calculate_covariance_matrix(matrix):
    rows, columns = get_dimemsions_from_matrix(matrix)
    matrix_transpose = np.matrix.transpose(matrix)
    if rows < columns:
        covariant_matrix = np.matmul(matrix, matrix_transpose)
    else:
        covariant_matrix = np.matmul(matrix_transpose, matrix)
    covariant_matrix = np.matmul(matrix, matrix_transpose, )
    return covariant_matrix


def return_nth_eigenvalue_eigenvector(number, eigenvalues, eivenvectors):
    nth_eigenvalues= eigenvalues[: number]
    nth_eigenvector = eivenvectors[:, number]
    return nth_eigenvalues, nth_eigenvector


def create_nth_reduced_matrix(reduction_number, matrix):
    return matrix[:reduction_number, :reduction_number]


def create_nth_reduced_diag_eigenvalue_matrix(reduction_number, eigenvalues):
    return np.sqrt(np.diag(eigenvalues[:reduction_number]))


def check_eigenvalue_eigenvector_with_matrix(eigenvalues, eigenvectors, matrix):
    """A*v = λ*v must be true with
    A: matrix
    v: eigenvector
    λ: eigenvalue
    """
    for col in range(len(matrix)):
        Av_eq_lambda_v = np.allclose(
            np.dot(matrix, eigenvectors[:, col]),
            np.dot(eigenvalues[col], eigenvectors[:, col]))
        if not Av_eq_lambda_v:
            message = f"A*v ≠ λ*v: eigenvector/eigenvalue with index {col} do not hold relationship"
            console.print(f"[red]{message}")


def data_must_have_float_entries(data):
    """as soon as element (can be array as well) is not a number alert is given"""
    to_check = np.isnan(data)
    if True in to_check:
        message = 'data corrupt'
        console.print(f"[red]{message}")


def list_eigenval__partial_energy__energy_ratio(eigenvalues, threshold=1):
    """
    - makes pretty table of eigenvalues and their 'weight'
    - threshold returns number of eigenvalues needed to have minimum energy level
    """
    log.info("rigid headers-variable leads to magic numbers in other functions.")
    headers = ('POD index', 'ith eigenvalue', 'part. energy', 'energy ratio', 'sigma=sqrt_of_lambda')
    A = compute__eigenval__partial_energy__energy_ratio(eigenvalues, headers)
    list_eigenval__partial_energy__energy_ratio_with_threshold(A, threshold, headers=headers)
    #save__eigenval__partial_energy__energy_ratio(A, headers)


def compute__eigenval__partial_energy__energy_ratio(eigenvalues, headers):
    """
    - calculates the relative importance of the i-th POD mode as np.matrix
    """
    log.info("fix magic numbers: so far order in header variable must match "
             "in loop...definitely error prone")
    number_of_eigenvalues = len(eigenvalues)
    total_energy = np.sum(eigenvalues)
    partial_energy = 0
    data_matrix = np.zeros((number_of_eigenvalues, len(headers)))

    for ith_eigenvalue in range(number_of_eigenvalues):
        partial_energy += eigenvalues[ith_eigenvalue]
        energy_ratio = partial_energy / total_energy
        data_matrix[ith_eigenvalue][0] = ith_eigenvalue
        data_matrix[ith_eigenvalue][1] = eigenvalues[ith_eigenvalue]
        data_matrix[ith_eigenvalue][2] = partial_energy
        data_matrix[ith_eigenvalue][3] = energy_ratio
        data_matrix[ith_eigenvalue][4] = np.sqrt(eigenvalues[ith_eigenvalue])
    return data_matrix


def list_eigenval__partial_energy__energy_ratio_with_threshold(matrix_a, threshold, headers):
    """
    - prints the eigenvalue-energy-relationship and returns the threshold value
      for energy ratio
    """
    log.info("to get threshold of required PODs rigid data structure MUST "
             "be passed that exact way => error prone and should be fixed")
    table_of_matrix = tabulate(matrix_a,
                    headers=headers,
                    tablefmt="simple",
                    floatfmt=(".0f", ".5e", ".2e", ".5e", ".5e"))
    console.print(f'[blue]{table_of_matrix}')

    console.print(f"[yellow]total Energy of System: "
                  f"{convert_to_scientific_notation(matrix_a[-2,-2],4)}")
    rows, _ = get_dimemsions_from_matrix(matrix_a)
    for i in range(rows):
        if matrix_a[i, 3] > threshold:
            console.print(f"[violet]including {i} POD index needed to "
                          f"guarantee min. threshold {threshold}: \n"
                          f"energy ratio {matrix_a[i, 3]} > threshold {threshold}")
            return
    console.print(f"[red]threshold value {threshold} seems to require all "
                  "eigenvalues; likely caused by floating comparison")


def save__eigenval__partial_energy__energy_ratio(matrix, headers):
    """
    - it is always good idea to have access to data in textfile-form
    - alternative that avoids pandas
        with open('table.txt', 'w') as f: f.write(tabulate(...))
      - see no big difference between both options...
    """
    df = pd.DataFrame(data=matrix, columns=headers, )
    format_mapping = {headers[0]: "{:.0f}",
                      headers[1]: "{:.10e}",
                      headers[2]: "{:.10e}",
                      headers[3]: "{:.10e}"}
    for key, value in format_mapping.items():
        df[key] = df[key].apply(value.format)
    df.to_csv('eigenval_partial_energy_energy_ratio.csv',
               sep='\t', index=False)


def create_full_Sigma_matrix(singular_values, rows=0):
    """
    - adds zero matrix with n rows to input matrix
               sigma_1          0      0           0
                     0    sigma_2      0           0
                   ...        ...    ...         ...
     Sigma =         0          0      0     sigma_n
                     0          0      0           0
                    ...        ...    ...         ...
                     0          0      0           0
    - default parameter leaves input matrix untouched
    """
    Sigma = np.diag(singular_values)
    _, columns = get_dimemsions_from_matrix(Sigma)
    return np.concatenate([Sigma, np.zeros((rows, columns))], axis=0)


def create_reduced_Sigma_matrix(singular_values):
    """
    - example with n different singular values
               sigma_1          0      0           0
     Sigma =         0    sigma_2      0           0
                   ...        ...    ...         ...
                     0          0      0     sigma_n
    """
    return np.diag(singular_values)


def return_reduced_matrix_from__U_S_Vstar(U, Sigma, V_star, rank):
    """returns reduced matrix R
    - X = U Sigma V_star    (SVD)
    - R = U Sigma V_star    (POD)
      BUT U, Sigma, V_star have reduced rank in computation for R
    """
    rows, _ = get_dimemsions_from_matrix(U)
    U = U[:rows, :rank]
    Sigma = Sigma[:rank, :rank]
    V_star = V_star[:rank, :rank]
    return np.matmul(U, np.matmul(Sigma, V_star))


def should_np_array_be_completely_displayed(status):
    """
    - when np.array is printed to console then for large matrices rows are
      skipped with ...(three dots)
    - this function let you switch between full or reduced console display
    """
    if status:
        np.set_printoptions(threshold=np.inf)


def set_number_of_digits_after_period(digits=8):
    """
    - toggle function to set number of digits of floates inside an array
    - does NOT affect bare floating point numbers
    """
    if (digits > 16) \
    or (digits < 0):
        message = 'WARNING: safety net triggered when number of digits was ' \
        'tried to be set.\n' \
        'Program continues with valid number.'
        console.print(f"[yellow]{message}")
        digits = 4
    np.set_printoptions(precision=digits)


def matrices_must_be_numerically_close(matrix_a, matrix_b):
    """
    - due to numeric reasons matrices can be 'equal' even when entries differ
      mathematically
    - so these two values for the same row & column in matrix_a and matrix_b
      are treated to be equal: 6.04347257e-14 and 0.00000000e+0
    - https://stackoverflow.com/questions/10851246/python-comparing-two-matrices
    """
    status = np.allclose(matrix_a, matrix_b)
    if status:
        console.print("[green]matrices are numerically close")
    else:
        console.print("[red]matrices are not numerically close")


def print_matrix_where_matrices_elements_are_close(matrix_a, matrix_b):
    """
    - mainly useful for debugging to check where two matrices differ
      numerically
    """
    console.print(f"{np.isclose(matrix_a, matrix_b)}")


def load_snapshot_matrix_from_comsol(file_to_load, dim=2):
    """
    - comsol data needs to be prepared for postprocessing, that involves to get
      rid of comments and to delete mesh coordinates
    - had issues with np.genfromtxt (less convenient) so I use np.loadtxt
    """
    log.info("when processing issues arise one day think about preparing data "
             "with awk/sed/perl in the first place")
    log.info("there's now a .sh file that provides the matrices from the"
             "exported data set, so a simple np.loadtxt is actually"
             "sufficient and this function a candidate to get sacked")
    #@ this solution suffers however from magigc numbers/restricted to 2d and
    #@ extra effort needed to generalize to 3d
    # awk '{ if($1 != "%"){ $1=$2=""; print $0}} OFS="\t"' input.txt > out.txt
    with open(file_to_load, 'r') as f:
        #? maybe create function like 'return_number_of_snapshots' for
        #? modular reasons
        number_of_comments=0
        for line in f:
            if line.startswith('%'):
                num_cols = len(f.readline().split())
                number_of_comments += 1
            #@ criterion to stop looking for comments because comsol has fixed 
            #@ structure and real data starts after metadata
            if not line.startswith('%'):  #
                break
        snapshot_matrix = np.loadtxt(file_to_load,
                          comments='%',
                          usecols=range(dim, num_cols))
        #@ not sure if useful in future => comment
        #@ function name must be adjunsted then for sure
        # mesh_coordinates = np.loadtxt(file_to_load,
        #                   comments='%',
        #                   usecols=range(0 , dim))
        return snapshot_matrix
