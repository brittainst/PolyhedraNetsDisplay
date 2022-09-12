#TODO: mini docstring

from functions import *
import random

name = input("Enter the type of polyhedra:")

#TODO: please make the if name thing universal. all these repeated lines are driving me crazy (if name)
numOfNets = 0
# This if statement sets two variables based on the type of net.
# numofnets is the total number of nets of that type
# k is the number of digits the number needs to have when it is part of the file name
if name == 'Tetrahedron':
    numOfNets = 2
    k = 1
elif name == 'Cube':
    numOfNets = 11
    k = 2
elif name == 'Octahedron':
    numOfNets = 11
    k = 2
elif name == 'Dodecahedron':
    numOfNets = 43380
    k = 5
else:
    numOfNets = 43380
    k = 5

# vcQuantity is a list/array that logs the number of nets with i vertex connections in the ith entry
vcQuantity = [0 for i in range(11)]
# vcIndex is a list/array that logs the numbers of all nets that have i vertex connections in the ith entry
vcIndex = [None for i in range(11)]

for i in range(0, numOfNets): # iterates through all nets
    # generates file name needed to call that net
    # .zfill(k) adds the number of zeros needed in the file name before the file number
    # loads the target file
    data = loadFile(name, str(i).zfill(k))
    v = np.array(data.get("Vertices"))  # Calls database entry as a list and then converts to an array
    e = np.array(data.get("Edges"))  # Calls database entry as a list and then converts to an array
    # calculates vertex score of the net we just pulled
    vertexScore = countVC(name, v, e, False)

    # adds 1 to the tally for how many nets there are with that many vertex connections
    vcQuantity[vertexScore] += 1

    # adds the number of that net to the corresponding row in the vcIndex
    if vcQuantity[vertexScore] == 1:
        vcIndex[vertexScore] = [i]
    else:
        vcIndex[vertexScore].append(i)
print(vcQuantity)
print(vcIndex)

# this for loop generates three random numbers of nets for each category of vertex score found
for i in range(0, len(vcQuantity)):
    if vcQuantity[i] != 0:
        x = random.randint(0, len(vcIndex[i]) - 1)
        y = random.randint(0, len(vcIndex[i]) - 1)
        z = random.randint(0, len(vcIndex[i]) - 1)
        net1 = vcIndex[i][x]
        net2 = vcIndex[i][y]
        net3 = vcIndex[i][z]
        print("Vertex Connections=" + str(i) + ": " + str([net1, net2, net3]))
