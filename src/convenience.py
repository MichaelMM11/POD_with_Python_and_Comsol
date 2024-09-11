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
import math
import numpy as np
import pandas as pd
from pathlib import Path
from tabulate import tabulate

def return_folder_dirs():
    current__dir = Path.cwd()
    main__dir = current__dir.parents[0]
    comsol__dir = main__dir.joinpath('comsol')
    data__dir = main__dir.joinpath('data')
    data_modes_dir = data__dir.joinpath('modes')
    src__dir = main__dir.joinpath('src')
    dirs = {}
    dirs['data'] = data__dir
    dirs['data_modes'] = data_modes_dir
    dirs['src'] = src__dir
    return dirs

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
    - log.warning("can be fixed quickly and no forced")
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


def print_dimemsions_from_matrix(matrix):
    """returns quick information of matrix dimensions"""
    rows, columns = get_dimemsions_from_matrix(matrix)
    print(f"number of rows:    {rows}\nnumber of columns: {columns}")


def should_np_array_be_completely_displayed(status):
    """
    - when np.array is printed to console then for large matrices rows are
      skipped with ...(three dots)
    - this function let you switch between full or reduced console display
    """
    if status:
        np.set_printoptions(threshold=np.inf)


def get_dimemsions_from_matrix(matrix):
    rows, columns = np.shape(matrix)[0], np.shape(matrix)[1]
    return rows, columns


def calculate_covariance_matrix(matrix):
    """
    - np.cov() does NOT yield results I get by hand calculation, so I stick to
      the definition
    """
    rows, cols = get_dimemsions_from_matrix(matrix)
    if not (rows > cols):
        message = "WARNING: rows > cols not fulfilled in covariance matrix"
        console.print(f"[yellow]{message}")
    return np.matmul(matrix.T, matrix)/(rows-1)


def calculate_stored_energy(eigenvalues):
    #! check if energy is same as 
    """
    - sum of eigenvalues of correlation matrix
    - eigenvalues no need to be sorted
    """
    #! another sourse states that E = np.sum(abs(eigenvalues))
    return np.sum(eigenvalues)


def sort_eigenvalues_eigenvectors(eigenval, eigenvec):
    idx = eigenval.argsort()[::-1]
    eigenValues = eigenval[idx]
    eigenVectors = eigenvec[:,idx]
    return eigenValues, eigenVectors


# def return_nth_eigenvalue_eigenvector(number, eigenvalues, eivenvectors):
#     nth_eigenvalues= eigenvalues[: number]
#     nth_eigenvector = eivenvectors[:, number]
#     return nth_eigenvalues, nth_eigenvector


# def create_nth_reduced_matrix(reduction_number, matrix):
#     return matrix[:reduction_number, :reduction_number]


# def create_nth_reduced_diag_eigenvalue_matrix(reduction_number, eigenvalues):
#     return np.sqrt(np.diag(eigenvalues[:reduction_number]))


# def check_eigenvalue_eigenvector_with_matrix(eigenvalues, eigenvectors, matrix):
#     """A*v = λ*v must be true with
#     A: matrix
#     v: eigenvector
#     λ: eigenvalue
#     """
#     for col in range(len(matrix)):
#         Av_eq_lambda_v = np.allclose(
#             np.dot(matrix, eigenvectors[:, col]),
#             np.dot(eigenvalues[col], eigenvectors[:, col]))
#         if not Av_eq_lambda_v:
#             message = f"A*v ≠ λ*v: eigenvector/eigenvalue with index {col} do not hold relationship"
#             console.print(f"[red]{message}")


# def data_must_have_float_entries(data):
#     """as soon as element (can be array as well) is not a number alert is given"""
#     to_check = np.isnan(data)
#     if True in to_check:
#         message = 'data corrupt'
#         console.print(f"[red]{message}")


def show_save_eigenvalue_energy_data(descending_eigenvalues, threshold=1):
    """
    - eigenvalues must be in descending order, otherwise GIGO
    #! - despite being a monolith and heavily violates the principle that a
    #!   function should do one and only ONE thing I keep this here as it is 
    #!   because of internal dependencies
    #! - the function can be divided into many smaller functions but each one
    #!   needs more than one input parameter and then the dependencies get
    #!   passed as returns and inputs parameter
    #!   => nothing gained at the end of the day except making things look more
    #!      complex than it actually is
    #! - as long as there is no need for improvement I think readability is
    #!   better given by this monolith and 
"""
    table_settings = {
        "POD":           {"col_position": 0, "notation": '.0f'},
        "eigenval":      {"col_position": 1, "notation": '0.6e'},
        "acc_eigenval":  {"col_position": 3, "notation": '0.3e'},
        "part_E":        {"col_position": 4, "notation": '0.3e'},
        "sigma":         {"col_position": 2, "notation": '0.6e'},
        "acc_part_E":    {"col_position": 5, "notation": '0.6f'},
        }

    #@ - make setup for internal variables
    number_of_columns = len(table_settings)
    number_of_eigenvalues = len(descending_eigenvalues)
    total_energy = np.sum(descending_eigenvalues)
    partial_energy = 0
    accumulated_partial_energy = 0
    acc_eigenval = 0
    data_matrix = np.zeros((number_of_eigenvalues, number_of_columns))


    #@ - column names and notations need to be sorted as declared in
    #@   table settings (this makes it easy in future version to add another)
    #@   column if needed without changing anything else
    #@ - this also makes table more dynamic and no magic numbers needed
    #@   (because single source of truth)
    col_positions = []
    notations = []
    for i in table_settings:
        notations.append(table_settings[i]['notation'])
        col_positions.append(table_settings[i]['col_position'])
    col_names = tuple(table_settings.keys())


    def check_if_columns_have_different_indices():
        for i in range(len(col_positions)):
            if i not in col_positions:
                message = 'WARNING: column header positions are not all ' \
                'different or first column does not start with index 0'
                console.print(f"[yellow]{message}")
                log.warning(message)
    check_if_columns_have_different_indices()


    #@ - needed because when indices are not in ascending order there is mismatch
    #@   between column names and values
    def sort_by_indexes(lst, indexes, reverse=False):
        #@ - https://www.w3resource.com/python-exercises/list/python-data-type-list-exercise-218.php
        return [val for (_, val) in sorted(zip(indexes, lst), key=lambda x: \
            x[0], reverse=reverse)]
    col_names = sort_by_indexes(col_names, col_positions)
    notations = sort_by_indexes(notations, col_positions)


    #@ - could actually add switch to decide if column should be printed or not
    #@   but that is 1) over-engineering and 2) not useful at all because at
    #@   later post-processing only the columns in need can be selected
    #@   to the actual computation; would only bloat code for smug satisfaction
    for i in range(number_of_eigenvalues):
        partial_energy = descending_eigenvalues[i] / total_energy
        accumulated_partial_energy += partial_energy
        acc_eigenval += descending_eigenvalues[i]

        data_matrix[i][table_settings["POD"]['col_position']] = i + 1
        data_matrix[i][table_settings["eigenval"]['col_position']] = descending_eigenvalues[i].real
        data_matrix[i][table_settings["sigma"]['col_position']] = np.sqrt(descending_eigenvalues[i]).real
        data_matrix[i][table_settings["part_E"]['col_position']] = partial_energy.real
        data_matrix[i][table_settings["acc_part_E"]['col_position']] = accumulated_partial_energy.real
        data_matrix[i][table_settings["acc_eigenval"]['col_position']] = acc_eigenval.real


    def return_POD_for_threshold_energy(threshold):
        if not (0 < threshold <= 1): 
            message = 'WARNING: threshold value not in (0,1]\n' \
            'program continues with threshold = 1'
            console.print(f"[yellow]{message}")
            log.warning(message)
            threshold = 1

        threshold_reached = False
        for i in range(number_of_eigenvalues):
            current_threshold_value = data_matrix[i][table_settings["acc_part_E"]['col_position']]
            if (current_threshold_value >= threshold) \
            and (not threshold_reached):
                console.print(f"[magenta]{i + 1} PODs needed to guarantee min "
                            f"threshold {threshold}: \n"
                            f"acc_part_E {current_threshold_value:.4f} >= threshold {threshold}")
                threshold_reached = True
    return_POD_for_threshold_energy(threshold)


    def check_if_accumulated_partial_energy_equals_one():
        """
        - it's never good idea to compare floats directly because of rounding
          errors
        - https://note.nkmk.me/en/python-math-isclose/
        """
        if not math.isclose(accumulated_partial_energy.real, 1, rel_tol=1e-3):
            message = 'ERROR: accumulated energy does not sum up to 1!\n' \
                    f'accumulated_partial_energy: {accumulated_partial_energy}'
            console.print(f"[red]{message}")
            log.error(message)
    check_if_accumulated_partial_energy_equals_one()


    def show_table_in_console(rows=11):
    #! - can be obsolete because all can be done in pandas
    #! - actually cleaner approach because "given on the fly"
        table_of_matrix = tabulate(
            data_matrix,
            headers=col_names,
            tablefmt="simple",
            floatfmt=notations)
        #@ - little workaround to show not all but the first n rows
        counter = 0
        for i in table_of_matrix.splitlines():
            counter += 1
            print(i)
            if counter == rows+2: return
        #console.print(f'[cyan]{table_of_matrix}')
    show_table_in_console()


    def save_table_to_file():
    #@ - have to modify notation of each column because tabulate asks for
    #@   different syntax than DataFrame
    #@ - https://stackoverflow.com/questins/32744997/apply-formatting-to-each-column-in-dataframe-using-a-dict-mapping
        folder_dir = return_folder_dirs()
        filename = 'eigenvalue_energy_table.dat'
        eigenvalue_energy_table = Path(folder_dir['data'], filename)
        df = pd.DataFrame(data=data_matrix, columns=col_names)
        panda_formatter = {}
        for i in table_settings:
            panda_formatter[i] = f"{{:{table_settings[i]['notation']}}}"
        format_mapping = panda_formatter
        for key, value in format_mapping.items():
            df[key] = df[key].apply(value.format)
        
        #@ - makes the function "show_table_in_console" obsolete and adds the
        #@   option to show not all columns but the first/last n ones
        #@ - only drawback is, that there are not separators between header
        #@   and data AND that the column width cannot be broader
        # console.print(f'[red]{df[:4]}') 
        
        df.to_csv(eigenvalue_energy_table, sep='\t', index=False)
    save_table_to_file()


# def create_full_Sigma_matrix(singular_values, rows=0):
#     """
#     - adds zero matrix with n rows to input matrix
#                sigma_1          0      0           0
#                      0    sigma_2      0           0
#                    ...        ...    ...         ...
#      Sigma =         0          0      0     sigma_n
#                      0          0      0           0
#                     ...        ...    ...         ...
#                      0          0      0           0
#     - default parameter leaves input matrix untouched
#     """
#     Sigma = np.diag(singular_values)
#     _, columns = get_dimemsions_from_matrix(Sigma)
#     return np.concatenate([Sigma, np.zeros((rows, columns))], axis=0)


def create_reduced_Sigma_matrix(singular_values):
    """
    - example with n different singular values
               sigma_1          0      0           0
     Sigma =         0    sigma_2      0           0
                   ...        ...    ...         ...
                     0          0      0     sigma_n
    """
    message = "WARNING: rename this function into telling name function"
    log.warning(message)
    return np.diag(singular_values)


# def return_reduced_matrix_from__U_S_Vstar(U, Sigma, V_star, rank):
#     """returns reduced matrix R
#     - X = U Sigma V_star    (SVD)
#     - R = U Sigma V_star    (POD)
#       BUT U, Sigma, V_star have reduced rank in computation for R
#     """
#     rows, _ = get_dimemsions_from_matrix(U)
#     U = U[:rows, :rank]
#     Sigma = Sigma[:rank, :rank]
#     V_star = V_star[:rank, :rank]
#     message = "WARNING: rename this function into telling name function"
#     log.warning(message)
#     return np.matmul(U, np.matmul(Sigma, V_star))


def matrices_must_be_numerically_close(matrix_a, matrix_b, rel_tol=1e-10):
    """
    - due to numeric reasons matrices can be 'equal' even when entries differ
      mathematically
    - so these two values for the same row & column in matrix_a and matrix_b
      are treated to be equal: 6.04347257e-14 and 0.00000000e+0
    - https://stackoverflow.com/questions/10851246/python-comparing-two-matrices
    """
    status = np.allclose(matrix_a, matrix_b, rtol=rel_tol)
    if status:
        console.print("[green]matrices are numerically close")
    else:
        console.print("[red]matrices are not numerically close")


# def print_matrix_where_matrices_elements_are_close(matrix_a, matrix_b):
#     """
#     - mainly useful for debugging to check where two matrices differ
#       numerically
#     """
#     console.print(f"{np.isclose(matrix_a, matrix_b)}")


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
    #@ - if converted to column vector by forxe "b = b.reshape(-1,1)" then a
    #@   lot of multiplications will break
    A = np.array([[0,1,3], [-2,3,4], [0,0,6]])
    B = np.array([[8,2,1], [3,1,0], [-5,2,7]])
    console.print(f"[blue]a = {a}\n")
    console.print(f"[yellow]b = {b}\n")
    console.print(f"[magenta]A =\n {A}\n")
    console.print(f"[cyan]B =\n {B}\n")
    separator()
    ab_matmul = np.matmul(a,b)
    ba_matmul = np.matmul(b,a)
    console.print(f"[blue]ab_matmul = {ab_matmul}\n")
    console.print(f"[blue]ba_matmul = {ba_matmul}\n")
    aA_matmul = np.matmul(a,A)
    Aa_matmul = np.matmul(A,a)
    console.print(f"[blue]aA_matmul = {aA_matmul}\n")
    console.print(f"[blue]Aa_matmul = {Aa_matmul}\n")
    AB_matmul = np.matmul(A,B)
    BA_matmul = np.matmul(B,A)
    console.print(f"[blue]AB_matmul =\n {AB_matmul}\n")
    console.print(f"[blue]BA_matmul =\n {BA_matmul}\n")
    separator()
    ab_multiply = np.multiply(a,b)
    ba_multiply = np.multiply(b,a)
    console.print(f"[green]ab_multiply = {ab_multiply}\n")
    console.print(f"[green]ba_multiply = {ba_multiply}\n")
    aA_multiply = np.multiply(a,A)
    Aa_multiply = np.multiply(A,a)
    console.print(f"[green]aA_multiply =\n {aA_multiply}\n")
    console.print(f"[green]Aa_multiply =\n {Aa_multiply}\n")
    AB_multiply = np.multiply(A,B)
    BA_multiply = np.multiply(B,A)
    console.print(f"[green]AB_multiply =\n {AB_multiply}\n")
    console.print(f"[green]BA_multiply =\n {BA_multiply}\n")
    separator()
    ab_dot = np.dot(a,b)
    ba_dot = np.dot(b,a)
    console.print(f"[yellow]ab_dot = {ab_dot}\n")
    console.print(f"[yellow]ba_dot = {ba_dot}\n")
    aA_dot = np.dot(a,A)
    Aa_dot = np.dot(A,a)
    console.print(f"[yellow]aA_dot = {aA_dot}\n")
    console.print(f"[yellow]Aa_dot = {Aa_dot}\n")
    AB_dot = np.dot(A,B)
    BA_dot = np.dot(B,A)
    console.print(f"[yellow]AB_dot =\n {AB_dot}\n")
    console.print(f"[yellow]BA_dot =\n {BA_dot}\n")
    separator()
    ab_inner = np.inner(a,b)
    ba_inner = np.inner(b,a)
    console.print(f"[cyan]ab_inner = {ab_inner}\n")
    console.print(f"[cyan]ba_inner = {ba_inner}\n")
    aA_inner = np.inner(a,A)
    Aa_inner = np.inner(A,a)
    console.print(f"[cyan]aA_inner = {aA_inner}\n")
    console.print(f"[cyan]Aa_inner = {Aa_inner}\n")
    AB_inner = np.inner(A,B)
    BA_inner = np.inner(B,A)
    console.print(f"[cyan]AB_inner =\n {AB_inner}\n")
    console.print(f"[cyan]BA_inner =\n {BA_inner}\n")
    separator()
    ab_outer = np.outer(a,b)
    ba_outer = np.outer(b,a)
    console.print(f"[violet]ab_outer =\n {ab_outer}\n")
    console.print(f"[violet]ba_outer =\n {ba_outer}\n")
    aA_outer = np.outer(a,A)
    Aa_outer = np.outer(A,a)
    console.print(f"[violet]aA_outer =\n {aA_outer}\n")
    console.print(f"[violet]Aa_outer =\n {Aa_outer}\n")
    AB_outer = np.outer(A,B)
    BA_outer = np.outer(B,A)
    console.print(f"[violet]AB_outer =\n {AB_outer}\n")
    console.print(f"[violet]BA_outer =\n {BA_outer}\n")


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


def k_th_U_matrix(A, eigenvector, k):
    """
    - returns the k_th contribution of the k_th eigenvalue/-vector
    """
    U_k = np.outer(A[:,k], eigenvector[:,k].T).real
    return U_k


def return_matrix_of_summarized_k_th_reduced_POD(A, eigenvector, k):
    rows, cols = get_dimemsions_from_matrix(A)

    if k >= max(rows,cols):
        message = f'WARNING: reduced rank was higher than max(rows, cols)' \
        f': {k} > max({rows},{cols})' \
        f'\nprogram continues with rank = {max(rows, cols)}'
        console.print(f"[yellow]{message}")
        log.warning(message)
        k = max(rows,cols)

    U_tilde = np.zeros((rows,cols))
    for k in range(k):
        U_k = k_th_U_matrix(A, eigenvector, k)
        U_tilde += U_k
    return U_tilde
