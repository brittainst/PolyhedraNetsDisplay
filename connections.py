from functions import *
import random

name = input("Enter the type of polyhedra:")

numofnets = 0
# This if statement sets two variables based on the type of net.
# numofnets is the total number of nets of that type
# k is the number of digits the number needs to have when it is part of the file name
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

# vcquantity is a list/array that logs the number of nets with i vertex connections in the ith entry
vcquantity = [0 for i in range(11)]
# vcindex is a list/array that logs the numbers of all nets that have i vertex connections in the ith entry
vcindex = [None for i in range(11)]

for i in range(0, numofnets): # iterates through all nets
    # generates file name needed to call that net
    # .zfill(k) adds the number of zeros needed in the file name before the file number
    filename = name + 'Net' + str(i).zfill(k) + '.json'
    # laods the target file
    data = loadfile(filename)
    v = np.array(data.get("Vertices"))  # Calls database entry as a list and then converts to an array
    e = np.array(data.get("Edges"))  # Calls database entry as a list and then converts to an array
    # calculates vertex score of the net we just pulled
    vertexscore = countvc(name,v,e, False)

    # adds 1 to the tally for how many nets there are with that many vertex connections
    vcquantity[vertexscore] += 1

    # adds the number of that net to the corresponding row in the vcindex
    if vcquantity[vertexscore] == 1:
        vcindex[vertexscore] = [i]
    else:
        vcindex[vertexscore].append(i)
print(vcquantity)
print(vcindex)

# this for loop generates three random numbers of nets for each category of vertex score found
for i in range(0, len(vcquantity)):
    if vcquantity[i] != 0:
        x = random.randint(0, len(vcindex[i]) - 1)
        y = random.randint(0, len(vcindex[i]) - 1)
        z = random.randint(0, len(vcindex[i]) - 1)
        net1 = vcindex[i][x]
        net2 = vcindex[i][y]
        net3 = vcindex[i][z]
        print("Vertex Connections=" + str(i) + ": " + str([net1, net2, net3]))
