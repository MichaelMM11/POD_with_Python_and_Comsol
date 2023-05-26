#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
purpose
    - interact with .mph files with .py script
      - modify .mph model
      - get stiffness matrix, vectors...

remark
    - be connected to university internet because of Comsol instance
    - https://mph.readthedocs.io/en/stable/tutorial.html
    - https://julianroth.org/res/Master_Thesis_Julian_Roth.pdf (for introduction)
"""

import mph
from pathlib import Path



current__dir = Path.cwd()
main__dir = current__dir.parents[0]
comsol__dir = main__dir.joinpath('comsol')

comsol_filename = 'Heat_Equation.mph'

file_to_load = Path(comsol__dir, comsol_filename)



client = mph.start()
model = client.load(file_to_load)
print(f"{client.names()}")















if __name__ == "__main__":
    print("Hello, World!")
