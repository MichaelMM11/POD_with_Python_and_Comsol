"""
- https://www.youtube.com/watch?v=cQwYmk3bMSo
- https://www.youtube.com/watch?v=Aua3eLpnGao
"""


# https://jontateixeira.github.io/posts/gmsh-exporting-old-msh-format/
# http://www.manpagez.com/info/gmsh/gmsh-2.2.6/gmsh_59.php#SEC59
import gmsh
import numpy as np

gmsh.initialize()
gmsh.open("trial.msh")



dim = -1
tag = -1
nodeTags, coords, parametricCoord = gmsh.model.mesh.getNodes(dim, tag)

cords = coords.reshape((-1,3))

xyz = coords.reshape(-1,3)
for tag, xyz_e in zip(nodeTags, xyz):
    print(f"Node # {tag} is at {xyz_e}")

defined_element_type = gmsh.model.mesh.getElementTypes()
print(f"{defined_element_type = }")

eletype = 2
tag = -1
eleTags, nodeTags = gmsh.model.mesh.getElementsByType(eletype, tag)

for tag, nodes in zip(eleTags, nodeTags):
    print(f"Element # {tag} has nodes {nodes}")




gmsh.finalize()
