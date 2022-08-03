from functions import *

name = input("Enter the type of polyhedra:")

numofnets = 0
# This if statement sets two variables based on the type of net.
# numofnets is the total number of nets of that type
# k is the number of digits the number needs to have when it is part of the file name
if name == 'Tetrahedron':
    numofnets = 2
    k = 1
    maxvc = 3
elif name == 'Cube':
    numofnets = 11
    k = 2
    maxvc = 4
elif name == 'Octahedron':
    numofnets = 11
    k = 2
    maxvc = 4
elif name == 'Dodecahedron':
    numofnets = 43380
    k = 5
    maxvc = 10
    maxvc = 10
else:
    numofnets = 43380
    k = 5
    maxvc = 8

array = [[0, 0] for i in range(numofnets)]
for i in range(0, numofnets):
    filename = name + 'Net' + str(i).zfill(k) + '.json'
    data = loadfile(filename)
    v = np.array(data.get("Vertices"))
    e = np.array(data.get("Edges"))
    f = np.array(data.get("Faces"))
    rg = radiusg(v, f)
    vc = countvc(name, v, e, False)
    array[i] = [vc, rg]

array2 = [None for i in range(0, maxvc + 1)]
for i in range(numofnets):
    pair = array[i]
    vc = pair[0]
    rg = pair[1]
    if array2[vc] == None:
        array2[vc] = [rg]
    else:
        array2[vc].append(rg)
print(array)
print(array2)
