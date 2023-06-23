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


def separator(msg="dummy"):
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


def load_snapshot_matrix_from_comsol(file):
    """
    - a simple load of file that expects data from comsol is preprocessed, i.e.
      all comments are removed as well as the first columns (s) that hold mesh
      points
    - if file contains however data that do not correspond to snapshots then
      there is no error thrown but will lead to wrong results at a later stage
    """
    return np.loadtxt(file)


def show_results_of_vector_matrix_multiplications():
    """
    - becaure there are more than one way how to multiply vectors and matrices
      and I ended up in confusion what operation is allowed and what is the
      result, I made this overview of provided multiplications to have some
      kind of reference for myself
    - I faced some invalid multiplications when I made a forced conversion of
      a vector to a matrix (check the other aux function for more information)
      and it turned out that things are not that easy as expected w.r.t input
      and output dimensions 
    - another reason is that there is no native row/column vector distinction
      i.e. both are treated as (x,) ndarray objects with x the number of their
      elements
    - message to take home: don't think of row/column vectors as special cases
      of a matrix and then everything is good; this is what I guessed would
      easily worked in the first place but it didn't; treat 1d arrays different
      than 2d arrays (sounds stupid but I had to learn/accept the hard way)
    """
    a = np.array([3,1,9])
    b = np.array([4,8,2])
    b = b.reshape(-1,1)
    M = np.array([[0,1,3], [-2,3,4], [0,0,6]])
    console.print(f"[blue]a = {a}")
    console.print(f"[yellow]b = {b}")
    console.print(f"[magenta]M =\n {M}")
    separator()
    ab_matmul = np.matmul(a,b)
    ba_matmul = np.matmul(b,a)
    console.print(f"[blue]ab_matmul = {ab_matmul}")
    console.print(f"[blue]ba_matmul = {ba_matmul}")
    aM_matmul = np.matmul(a,M)
    Ma_matmul = np.matmul(M,a)
    console.print(f"[blue]aM_matmul = {aM_matmul}")
    console.print(f"[blue]Ma_matmul = {Ma_matmul}")
    separator()
    ab_multiply = np.multiply(a,b)
    ba_multiply = np.multiply(b,a)
    console.print(f"[green]ab_multiply = {ab_multiply}")
    console.print(f"[green]ba_multiply = {ba_multiply}")
    aM_multiply = np.multiply(a,M)
    Ma_multiply = np.multiply(M,a)
    console.print(f"[green]aM_multiply =\n {aM_multiply}")
    console.print(f"[green]Ma_multiply =\n {Ma_multiply}")
    separator()
    ab_dot = np.dot(a,b)
    ba_dot = np.dot(b,a)
    console.print(f"[yellow]ab_dot = {ab_dot}")
    console.print(f"[yellow]ba_dot = {ba_dot}")
    aM_dot = np.dot(a,M)
    Ma_dot = np.dot(M,a)
    console.print(f"[yellow]aM_dot = {aM_dot}")
    console.print(f"[yellow]Ma_dot = {Ma_dot}")
    separator()
    ab_inner = np.inner(a,b)
    ba_inner = np.inner(b,a)
    console.print(f"[cyan]ab_inner = {ab_inner}")
    console.print(f"[cyan]ba_inner = {ba_inner}")
    aM_inner = np.inner(a,M)
    Ma_inner = np.inner(M,a)
    console.print(f"[cyan]aM_inner = {aM_inner}")
    console.print(f"[cyan]Ma_inner = {Ma_inner}")
    separator()
    ab_outer = np.outer(a,b)
    ba_outer = np.outer(b,a)
    console.print(f"[violet]ab_outer =\n {ab_outer}")
    console.print(f"[violet]ba_outer =\n {ba_outer}")
    aM_outer = np.outer(a,M)
    Ma_outer = np.outer(M,a)
    console.print(f"[violet]aM_outer =\n {aM_outer}")
    console.print(f"[violet]Ma_outer =\n {Ma_outer}")


def show_results_of_array_reshaping():
    """
    - originally 1d arrays behave differently than 2d arrays and I happened to
      encounter confusion when I wanted to multiply such 1d array with 2d
      array
      so I started to make a 'forced' conversion of a 1d array to a 2d array
      with the result that I (again) had results that I didn't expect in the
      first place
    - this overview shows what happens to a 1d array when its subjected to
      dimension transform
      as you can expect this new object does NOT behave in the same way as a
      1d array object does and not all multiplications are supported that
      worked perfectly fine for the original 1d array
    - triggered by that 
    - what's lesson learnt? Quite simple: just don't do any forced conversion
      to have all objects with well-defined np.shape(obj)[0] and
      np.shape(obj)[1] values to get the convenient feedback if object is row
      or column vector; in this case don't think of row/column vector as
      special case of matrix and everything is good, take them as two different
      kind of objects (even though it's temptating)
    """
    separator("starting with (native) row array")
    a = np.array([3,1,9])
    console.print(f"[blue]a = {a}")
    console.print(f"[blue]shape_a = {np.shape(a)}")
    separator("after a.np.reshape(1,-1)")
    b = a.reshape(1,-1)
    console.print(f"[green]b = {b}")
    console.print(f"[green]shape_b = {np.shape(b)}")
    separator("after a.np.reshape(-1,1)")
    c = a.reshape(-1,1)
    console.print(f"[yellow]c = {c}")
    console.print(f"[yellow]shape_c = {np.shape(c)}")

    separator("now new array, not row but column, created with reshape(-1,1)")

    d = np.array([3,1,9])
    d = d.reshape(1,-1)
    console.print(f"[blue]d = {d}")
    console.print(f"[blue]shape_d = {np.shape(d)}")
    separator("after d.np.reshape(1,-1)")
    e = d.reshape(1,-1)
    console.print(f"[green]e = {e}")
    console.print(f"[green]shape_e = {np.shape(e)}")
    separator("after d.np.reshape(-1,1)")
    f = d.reshape(-1,1)
    console.print(f"[yellow]f = {f}")
    console.print(f"[yellow]shape_f = {np.shape(f)}")
