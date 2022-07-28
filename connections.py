from functions import *
import random

name = input("Enter the type of polyhedra:")

numofnets = 0
if name == 'Tetrahedron':
    numofnets = 2
    k = 1
elif name == 'Cube':
    numofnets = 11
    k = 2
elif name == 'Octahedron':
    numofnets = 11
    k = 2
elif name == 'Dodecahedron':
    numofnets = 43380
    k = 5
else:
    numofnets = 43380
    k = 5

vcquantity = [0 for i in range(11)]
vcindex = [None for i in range(11)]

for i in range(0, 3000):
    print(i)
    data = loadfile(name,str(i).zfill(k))
    v = np.array(data.get("Vertices"))  # Calls database entry as a list and then converts to an array
    e = np.array(data.get("Edges"))  # Calls database entry as a list and then converts to an array
    vertexscore = countvc(name,v,e)
    vcquantity[vertexscore] += 1
    if vcquantity[vertexscore] == 1:
        vcindex[vertexscore] = [i]
    else:
        vcindex[vertexscore].append(i)
print(vcquantity)
print(vcindex)

for i in range(0, len(vcquantity)):
    if vcquantity[i] != 0:
        x = random.randint(0, len(vcindex[i]) - 1)
        y = random.randint(0, len(vcindex[i]) - 1)
        z = random.randint(0, len(vcindex[i]) - 1)
        net1 = vcindex[i][x]
        net2 = vcindex[i][y]
        net3 = vcindex[i][z]
        print("Vertex Connections=" + str(i) + ": " + str([net1, net2, net3]))
