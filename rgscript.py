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

# creates an empty array to store [number of vertex connections, radius of gyration] for each net
array = [[0, 0] for i in range(numofnets)]

# for each Dürer net
for i in range(0, numofnets):
    # Loads appropriate file as a dictionary
    filename = name + 'Net' + str(i).zfill(k) + '.json'
    data = loadfile(filename)

    v = np.array(data.get("Vertices"))  # stores vertices
    e = np.array(data.get("Edges"))  # stores edges
    f = np.array(data.get("Faces"))  # stores faces
    rg = radiusg(v, f)  # tabulates radius of gyration
    vc = countvc(name, v, e, False)  # tabulates number of vertex connections
    array[i] = [vc, rg]  # adds [number of vertex connections, radius of gyration to the corresponding entry in array

# array2 is going to store the radius of gyration data, but each row is only radius of gyration data for that number
# of vertex connections
array2 = [None for i in range(0, maxvc + 1)]

# for each net
for i in range(numofnets):
    pair = array[i]
    vc = pair[0]  # pulls out vertex connections for that net
    rg = pair[1]  # pulls out radius of gyration for that net
    if array2[vc] == None:  # If the row for that number of Vc is empty, the radius of gyration starts that row
        array2[vc] = [rg]
    else:  # If the row for that number of Vc is not empty, the radius of gyration is appended to that row
        array2[vc].append(rg)

# prints both arrays
print(array)
print(array2)

# prints the len of each
for i in len(array):
    print("n = " + str(len(array2[i])))
