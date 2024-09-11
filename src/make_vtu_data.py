#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
purpose
    - creates aux-files that contain for all snapshots data over geometry/mesh
    - the content of such a file can then easily inserted into .vtu-file
        (so far tedious to do by hand but more than sufficient for prototyping)

untested source
    import meshio
    import vtk.vtk
    https://stackoverflow.com/questions/54044958/reading-data-from-a-raw-vtk-vtu-file
"""

from convenience import *
from pathlib import Path
import csv


def split_float(number):
    """
    - splits float into parts before and after decimal point
    """
    #@ - https://stackoverflow.com/questions/3886402/how-to-get-numbers-after-decimal-point
    if not isinstance(number, float):
        message = 'WARNING: in split float'
        console.print(f"[yellow]{message}")
        log.warning(message)
    before_dot, after_dot = 0, 0
    if '.' in str(number):
        before_dot, after_dot = str(number).split('.')
    return before_dot, after_dot

def get_timestamps_from_file(filename="from_Comsol_odd_timesteps.vtu"):
    """
    - reads vtu file and returns all timestamps if file is result of transient
        simulation
    """
    # regex expressions like
    #    timestamp = re.findall(r'[0-9]+\.[0-9]+', line)
    #    timestamp = re.findall(r'\d*\.?\d+', line)
    # feel too cumbersome
    #@ - https://stackoverflow.com/questions/4703390/how-to-extract-a-floating-number-from-a-string
    vtu_file = Path(data__dir, filename)
    timestamp_values = []
    with open (vtu_file,'r') as file:
        lines = file.readlines()
        for line in lines:
            if "_@_t=" in line:  #if line.startswith('<DataArray type="Float64" Name="Temperature_@_t'):
                start_excluding = '_@_t='
                end_excluding = '\" '
                #@ - https://stackoverflow.com/questions/3368969/find-string-between-two-substrings
                timestamp_as_str = line[line.find(start_excluding)
                                        + len(start_excluding):line.rfind(end_excluding)]
                timestamp_as_float = float(timestamp_as_str)
                timestamp_values.append(timestamp_as_float)
    return timestamp_values

def return_max_digits_left_to_decimal_point(floatings):
    """
    - return max digits left to decimal point (works on positive and negative numbers)
    - implementation 
            len(str(int(max(list(map(abs, floatings))))))
        is ugly but does indeed the job; nevertheless more declarative solution
        is chosen for readability
    """
    #@ - https://stackoverflow.com/questions/2189800/how-to-find-length-of-digits-in-an-integer
    #@ - hilarious discussion about pros and cons suggestions
    max_digits = 0
    for i in floatings:
        positive_int = int(abs(i))
        current_digits = len(str(positive_int))
        if current_digits > max_digits:
            max_digits = current_digits
    return max_digits

def convert_timestamps_to_padded_timestamps(floatings):
    timestamp_as_paddded = []
    digits_to_pad = return_max_digits_left_to_decimal_point(floatings)
    for i in floatings:
        before_dot, after_dot = split_float(i)
        before_dot = str(before_dot).zfill(digits_to_pad)
        if before_dot.startswith('-') \
        and len(before_dot) == digits_to_pad:
            #@ - negative numbers needs special care because the minus sign
            #@     takes up one digit and this missing 0 must be added manually
            before_dot = before_dot[0] + '0' + before_dot[1:]
        padded_number = before_dot + '.' + str(after_dot)
        timestamp_as_paddded.append(padded_number)
    return timestamp_as_paddded

def create_aux_padded_timestamp_data_files(quantity):
    """
    - prepare auxiliary files that are needed for postprocessing
    - data values are grouped with 
        <DataArray type="Float64" Name="Temperature_@_t=00.0" Format="ascii">
        2.800773486346740242e+02
        2.426489604493093566e+02
        2.800773486346745926e+02
        ...
        </DataArray>
    - this structure is creatd for each timestamp, note that the quantity can
        be adjusted
    - padded timestamps make further visualization in paraview convenient as
        the lexical ordering is changed to semantic ordering (what you expect,
        so that timestamp 11 is later listed than timestamp 9)
    """
    end_marker = f'</DataArray>'
    counter = 0
    for path in pathlist:
        counter += 1
        filename = f'vtu_preparation_for_{counter}modes.dat'
        data_file = Path(data__dir, filename)
        with open (data_file, 'w') as file:
            for idx, i in enumerate(padded_timestamps):  #@ to guarantee that all timestemps are iterated
                start_marker = f'<DataArray type="Float64" Name="{quantity}_@_t={i}" Format="ascii">'
                file.write(start_marker + '\n')
                with open(path, 'r',) as csv_input:
                    for row in csv.reader(csv_input, delimiter='\t'):
                        file.write(row[idx] + '\n')
                file.write(end_marker + '\n')

def remove_timestemps_from_vtu(filename="from_Comsol_odd_timesteps.vtu"):
    """
    - returns the bare vtu content from input file EXCEPT the '<DataArray> and
        </DataArray>' groups with data values
    """
    input_filename = filename
    input_file = Path(data__dir, input_filename)
    output_file = Path(data__dir, 'bare_vtu.vtu')
    is_line_written = 'yes'
    with open (input_file, 'r') as file_to_read:
        with open (output_file, 'w') as file_to_write:
            lines = file_to_read.readlines()
            for line in lines:
                if is_line_written == 'yes':
                    file_to_write.write(line)
                if line.startswith('<PointData>'):
                    is_line_written = 'no'
                    file_to_write.write('\n')
                if line.startswith('</PointData>'):
                    is_line_written = 'yes'
                    file_to_write.write('</PointData>\n')

def generate_vtu_from_prepared_dat_and_bare_vtu():
    """
    - two aux files (bare vtu and prepared dat) are merged to one valid vtu file
        that can be inspected with paraview
    - idea is that visualization is much easier with padded timestamps because
        the lexical ordering is changed to semantic ordering (what you expect,
        so that timestamp 11 is later listed than timestamp 9)
    TODO: Think how hardcoded values can be cleaned
    """
    bare_vtu_file = Path(data__dir, 'bare_vtu.vtu')
    pathlist = sorted(Path(data__dir).rglob('vtu_preparation_for_*'))
    #@ - should be in regex form, it's in your interest to be generic
    counter = 0
    for path in pathlist:
        counter += 1
        path_in_str = str(path)
        with open (bare_vtu_file, 'r') as file_to_read:
            vtu_mode_file = Path(data__dir, f'vtu_for_{counter}modes.vtu')
            with open(vtu_mode_file, 'w',) as file_to_write:
                lines = file_to_read.readlines()
                for line in lines:
                    if line.strip() == '':
                        with open(path_in_str, 'r', encoding='utf-8') as file:
                            x = file.readlines()
                            for y in x:
                                if line.strip() == '':
                                    file_to_write.write(y)
                    else:
                        file_to_write.write(line)


def get_quantity_from_file(filename="from_Comsol_odd_timesteps.vtu"):
    vtu_file = Path(data__dir, filename)
    with open(vtu_file, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if line.startswith('<DataArray'):
                start_excluding = ' Name='
                end_excluding = '_@_t='  #'\" '
                #@ - https://stackoverflow.com/questions/3368969/find-string-between-two-substrings
                quantity_name = line[line.find(start_excluding) +1  # because " in string
                                        + len(start_excluding):line.rfind(end_excluding)]
                break
    return quantity_name

folder_dir = return_folder_dirs()
data__dir = folder_dir['data']
pathlist = sorted(Path(data__dir).rglob('reduced_matrix_of_*'))
timestamp_vtu = get_timestamps_from_file("from_Comsol_odd_timesteps.vtu")
padded_timestamps = convert_timestamps_to_padded_timestamps(timestamp_vtu)


quantity = get_quantity_from_file()
create_aux_padded_timestamp_data_files(quantity)
remove_timestemps_from_vtu()
generate_vtu_from_prepared_dat_and_bare_vtu()


# if __name__ == "__main__":
#     folder_dir = return_folder_dirs()
#     data__dir = folder_dir['data']

#     pathlist = sorted(Path(data__dir).rglob('reduced_matrix_of_*'))
#     #@ - should be in regex form, it's in your interest to be generic


#     timestamp_vtu = get_timestamps_from_file("from_Comsol_odd_timesteps.vtu")

#     # a = list(map(float, [-300.0, 2.8, 0.0, 3.3, 123.456, 12345]))  # [[float(i) for i in a]]
#     padded_timestamps = convert_timestamps_to_padded_timestamps(timestamp_vtu)

#     create_aux_padded_timestamp_data_files()
#     remove_timestemps_from_vtu()
#     generate_vtu_from_prepared_dat_and_bare_vtu()
#     print("Hello, World!")
