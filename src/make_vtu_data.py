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
    #! make function like: convert number with padding zeros(number, paddings)
    before, after = 0, 0
    if '.' in str(x):
        before, after = str(x).split('.')
    return before, after
    #return int(before), (int(after)*10 if len(after)==1 else int(after))




def get_timestamp_as_list():
    #! - so far timestamps are stored as string and not floats...
    #! - does not harm but should be fixed for correctness
    import re
    vtu_data = Path(data__dir, "from_Comsol_odd_timesteps.vtu")
    timestamp_lst = []
    with open (vtu_data,'r') as f:
        lines = f.readlines()
        for line in lines:
            #if line.startswith('<DataArray type="Float64" Name="Temperature_@_t'):
            if "_@_t=" in line:
                #timestamp = re.findall(r'[0-9]+\.[0-9]+', line)
                #timestamp = re.findall(r'\d*\.?\d+', line)  #@ alternative
                #@ - https://stackoverflow.com/questions/4703390/how-to-extract-a-floating-number-from-a-string
                start = '_@_t='
                end = '\" '
                timestamp_as_str = line[line.find(start) + len(start):line.rfind(end)]
                #@ - https://stackoverflow.com/questions/3368969/find-string-between-two-substrings
                timestamp_as_float = float(timestamp_as_str)
                timestamp_lst.append(timestamp_as_float)
    timestamp_value = []
    return timestamp_value
timestamp_vtu = get_timestamp_as_list()

#! convert list to floats
a = list(map(float, [30.0, 2.8, 0.0, 3.3, 12, 123.456, 12]))  # [[float(i) for i in a]]

#! return max digits left to decimal point (works on positive and negative numbers)
digits_to_pad = len(str(int(max(list(map(abs, a))))))  #! ugly but it does indeed the job
print(digits_to_pad)
#@ - https://stackoverflow.com/questions/2189800/how-to-find-length-of-digits-in-an-integer
#@ - hilarious discussion about pros and cons suggestions

timestamp_as_paddded = []
for i in a:
    a,b = split_float(str(i))
    a = str(a).zfill(digits_to_pad)
    if a.startswith('-'):
        a = a[0] + '0' + a[1:]
    padded_number = a + '.' + str(b)
    timestamp_as_paddded.append(padded_number)

print(timestamp_as_paddded)


exit()


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

if __name__ == "__main__":
    print("Hello, World!")
    #! useful here because of aux script