#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
purpose
    - this file creates all reduced timesteps-vtu that is needed to load all
        of them into paraview so you can have an animation out of the box
    - vtu-input can be taken from Comsol export, that's all needed

background
    - you CANNOT make animation when time is explicit in vtu-DataArray
    - you WANT to get the time order of files, so it MUST be part of filename
    - you HAVE TO have some roudabout for proper order
    - don't forget to select the colouring in the "properties" left the pane,
        then click on "Play" in the top panel bar
    - needs heavily getting clean coded
"""

from convenience import *
import numpy as np
from pathlib import Path
import decimal  # https://stackoverflow.com/questions/25099626/convert-scientific-notation-to-float

#<DataArray type="Float64" Name="Magnetic_flux_density_norm_@_t=0" Format="ascii">

folder_dir = return_folder_dirs()
data__dir = folder_dir['data']
filename = 'from_Comsol_odd_timesteps_backup.vtu'
filename = 'vtu_for_3modes.vtu'
input_filename = 'from_Comsol_odd_timesteps.vtu'

def get_quantity_from_file(filename=input_filename):
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


def get_timestamps_from_file(filename=input_filename):
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
    timestamp_in_vtu = []
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
                timestamp_in_vtu.append(timestamp_as_str)
                timestamp_values.append(timestamp_as_float)
    return timestamp_values, timestamp_in_vtu


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

quantity_name = get_quantity_from_file(filename)
print(quantity_name)

# TODO make more adaptive to name
modes = (int(''.join(filter(str.isdigit, filename))))
quantity_name = "_".join([quantity_name, str(modes), 'modes'])
foldername = "_".join(['anime_', quantity_name])
quantity_folder = folder_dir['data'].joinpath(foldername)
quantity_folder.mkdir(exist_ok=True)

timestamps_as_float, timestamps_in_vtu = get_timestamps_from_file(filename)
#print(timestamps_in_vtu)


timestamps_for_files = []
for i in timestamps_as_float:
    a = np.format_float_positional(i)
    a = str(a)
    x = a.replace('.', '_')
    if x.endswith('_'):
        x += '0'
    x = "__" + x
    timestamps_for_files.append(x)



filename_in_dir = []
for i,j in zip(timestamps_for_files, timestamps_in_vtu):
    if len(timestamps_for_files) != len(timestamps_in_vtu):
        print("both lists are not identical")
        exit()

    name = quantity_name + i +'.vtu'
    print(f"{name = }")
    print()

    filepath = quantity_folder / name  #! TODO make from_Comsol_vtu essential to name as several vtu exist (just remove .vtu from name)
    print(filepath)
    print()
    filename_in_dir.append(filepath)
    filepath.touch()
    vtu_file = Path(data__dir, filename)

    with open(vtu_file,'r') as firstfile, open(filepath,'w') as secondfile:
        block_of_interest_active = False
        fake_block_active = False
        outside_block = True
        #print(f"{quantity_name} for t={j} done")
        for line in firstfile:
            """
            0.0009
            first: 2.097248667653672E-4
            last: 0.08650071100495024
            """

            if line.startswith('<DataArray'):
                if f'_@_t={j}"' in line:
#                    print('1', line)
                    line = line.replace(f"={j}", '')  # because no time must be given explicit, otherwise paraview doesn't handle it properly and shows grey block
                    block_of_interest_active = True
                    fake_block_active = False
                    outside_block = False
                elif f'_@_t=' in line:
#                    print('2', line)
                    fake_block_active = True
                    outside_block = False
                else:
#                    print('3', line)
                    block_of_interest_active = False
                    fake_block_active = False
                    outside_block = True

            if fake_block_active and \
            line.startswith('</DataArray>'):
                fake_block_active = False
                outside_block = True
                continue

            if fake_block_active:
                continue

            if block_of_interest_active and \
            line.startswith('</DataArray>'):
                secondfile.write(line)
                block_of_interest_active = False
                outside_block = True
                continue

            if block_of_interest_active:
                secondfile.write(line)
                continue

            if outside_block:
                secondfile.write(line)

