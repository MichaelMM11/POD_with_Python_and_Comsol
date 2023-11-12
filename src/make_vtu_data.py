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

folder_dir = return_folder_dirs()
data__dir = folder_dir['data']

pathlist = sorted(Path(data__dir).rglob('reduced_matrix_of_*'))
#@ - should be in regex form, it's in your interest to be generic


def split_float(x):
    '''split float into parts before and after the decimal
    https://stackoverflow.com/questions/3886402/how-to-get-numbers-after-decimal-point'''
    before, after = 0, 0
    if '.' in x:
        before, after = str(x).split('.')
    return before, after
    #return int(before), (int(after)*10 if len(after)==1 else int(after))




def get_timestamp_as_list():
    #! - so far timestamps are stored as string and not floats...
    #! - does not harm but should be fixed for correctness
    import re
    vtu_data = Path(data__dir, "from_Comsol_odd_timesteps.vtu")
    timestamp_line = []
    timestamp_tuple = []
    with open (vtu_data,'r') as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith('<DataArray type="Float64" Name="Temperature_@_t'):
                #? - think if Name="Temperature_@_t is actually needd
                #timestamp = re.findall(r'[0-9]+\.[0-9]+', line)
                timestamp = re.findall(r'\d*\.?\d+', line)  #@ alternative
                #@ - https://stackoverflow.com/questions/4703390/how-to-extract-a-floating-number-from-a-string
                #@ - needs postprocessing but does the job
                timestamp_line.append(line)
                timestamp_tuple.append(timestamp)
    timestamp_value = []
    for i in timestamp_tuple:
        timestamp_value.append(i[1])
    #@ - values can also be written with leading zeros but skipped for the moment
    # for i in a:
    #     print(i.zfill(5))
    return timestamp_line, timestamp_value
timestamp_line, timestamp_vtu = get_timestamp_as_list()


end = f'</DataArray>'
counter = 0
for path in pathlist:
    counter += 1
    filename = f'vtu_preparation_for_{counter}modes.dat'
    data_file = Path(data__dir, filename)
    with open (data_file,'w') as f:
        for idx, i in enumerate(timestamp_vtu):  #@ to guarantee that all timestemps are iterated
            #print(i)
            a,b = split_float(i)
            #print(a,b)
            a = str(a).zfill(2)  #! magic number can be eliminated by take the length before floating point
            #! period, save this value and insert here
            #print(a)
            padded_number = a + '.' + str(b)
            #print(number)
            start = f'<DataArray type="Float64" Name="Temperature_@_t={i}" Format="ascii">'
            #! parse data file and adjust time value - with padding if needed
            f.write(start + '\n')
            with open(path, 'r',) as csv_input:
                for row in csv.reader(csv_input, delimiter='\t'):
                    f.write(row[idx] + '\n')
            f.write(end + '\n')


input_filename = 'from_Comsol_odd_timesteps.vtu'
#data__dir = folder_dir['data']
input_file = Path(data__dir, input_filename)
output_file = Path(data__dir, 'bare_vtu.vtu')
def comsol_vtu_but_no_timestemps():
    is_line_written = 'yes'
    with open (input_file,'r') as file:
        with open (output_file, 'w') as f:
            lines = file.readlines()
            for line in lines:
                if is_line_written == 'yes':
                    f.write(line)
                if line.startswith('<PointData>'):
                    is_line_written = 'no'
                    f.write('\n')
                if line.startswith('</PointData>'):
                    is_line_written = 'yes'
                    f.write('</PointData>\n')
comsol_vtu_but_no_timestemps()



pathlist = sorted(Path(data__dir).rglob('vtu_preparation_for_*'))  #! sorted can be actually removed
#@ - should be in regex form, it's in your interest to be generic
counter = 0
for path in pathlist:
    counter += 1
    path_in_str = str(path)
    with open (output_file, 'r') as f:
        a_file = Path(data__dir, f'vtu_for_{counter}modes.vtu')
        with open(a_file,'w',) as dum:
            lines = f.readlines()
            for line in lines:
                if line.strip() == '':
                    with open(path_in_str,'r', encoding='utf-8') as file:
                        x = file.readlines()
                        for y in x:
                            if line.strip() == '':
                                dum.write(y)
                else:
                    dum.write(line)
