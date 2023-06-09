#!/usr/bin/env python3
# -*- coding:utf-8 -*-



"""
purpose
    - 

remark
    - 
"""




def inspect(x):
    """returns quick&dirty main information of variable"""
    print(type(x))
    print(x)


""" 
- creates file where information during runtime is tracked
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
    format='%(asctime)s  [%(levelname)-8s] %(lineno)7s : %(message)s',
    filemode='a',
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


"""time
  - time speed of function calls are of interest, this wrapper is most useful
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
        console.print(f"[blue]Wrapper computation time:", elapsed, "s")
        return result
    return wrapper



"""numbers
"""
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
    console.print(f"[yellow] Absolute error:", abs_err)
    console.print(f"[yellow] Relative error:", rel_err, "%")




"""matrix
"""
import numpy as np
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
    covariant_matrix = np.matmul(matrix,matrix_transpose, )
    return covariant_matrix

def return_nth_eigenvalue_eigenvector(number, eigenvalues, eivenvectors):
    nth_eigenvalues= eigenvalues[:number]
    nth_eigenvector = eivenvectors[:,number]
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
            np.dot(matrix, eigenvectors[:,col]),
            np.dot(eigenvalues[col], eigenvectors[:,col]))
        if not Av_eq_lambda_v:
            message = f"A*v ≠ λ*v: eigenvector/eigenvalue with index {col} do not hold relationship"
            console.print(f"[red]{message}")



"""
data
"""
import numpy as np
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
    number_of_eigenvalues = len(eigenvalues)
    total_energy = np.sum(eigenvalues)
    partial_energy = 0

    console.print(f"[yellow]POD index ith eigenvalue part. energy   energy ratio")
    console.print(f"[yellow]{9*'='} {14*'='} {12*'='}   {12*'='}")
    for ith_eigenvalue in range(number_of_eigenvalues):
        partial_energy += eigenvalues[ith_eigenvalue]
        energy_ratio = partial_energy/total_energy

        console.print(f"{ith_eigenvalue:2} " \
              f"       {convert_to_scientific_notation(eigenvalues[ith_eigenvalue], 4)} " \
              f"   {convert_to_scientific_notation(partial_energy, 4)} " \
              f"   {convert_to_scientific_notation(energy_ratio, 4)} ")
    if energy_ratio > threshold:
        console.print(f"[violet]threshold = {threshold} => {ith_eigenvalue+1} PODs sufficient")
        #     return  #@ lead to unwanted cut-off


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
    return np.concatenate([Sigma, np.zeros((rows,columns))], axis=0)


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
    - when np.array is printed to console then for large matrices rows are skipped
    with ...
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
        message = 'WARNING: safety net triggered when number of digits was tried to be set.\n' \
        'Program continues with valid number.'
        console.print(f"[yellow]{message}")
        digits = 4
    np.set_printoptions(precision=digits)

def matrices_must_be_numerically_close(matrix_a, matrix_b):
    """
    - due to numeric reasons matrices can be 'equal' even when entries differ 
      mathematically
    - so these two values for the same row & column in matrix_a and matrix_b are
      treated to be equal: 6.04347257e-14 and 0.00000000e+0
    - https://stackoverflow.com/questions/10851246/python-comparing-two-matrices
    """
    status = np.allclose(matrix_a, matrix_b)
    if status:
        console.print(f"[green]matrices are numerically close") 
    else:
        console.print(f"[red]matrices are not numerically close") 

def print_matrix_where_matrices_elements_are_close(matrix_a, matrix_b):
    """
    - mainly useful for debugging to check where two matrices differ numerically
    """
    console.print(f"{np.isclose(matrix_a, matrix_b)}")