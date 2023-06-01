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
    text = f"[blue]↓ {msg} ↓"
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
    matrix_transpose = np.matrix.transpose(matrix)
    return np.matmul(matrix_transpose, matrix)

def return_nth_eigenvalue_eigenvector(number, eigenvalues, eivenvectors):
    nth_eigenvalues= eigenvalues[:number]
    nth_eigenvector = eivenvectors[:,number]
    return nth_eigenvalues, nth_eigenvector

def create_nth_reduced_matrix(reduction_number, matrix):
    return matrix[:reduction_number, :reduction_number]

def create_nth_reduced_diag_eigenvalue_matrix(reduction_number, eigenvalues):
    return np.diag(eigenvalues[:reduction_number])

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
            return