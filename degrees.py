from functions import *

#TODO: if name
name = input("Enter the type of polyhedra:")

numOfNets = 0
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

distLog = np.zeros((30, 5)).astype(int)
quantityLog = np.zeros((30, 1)).astype(int)
indexLog = [None for i in range(21)]

for i in range(0, numOfNets):
    dist = giveDegDist(name, str(i).zfill(k))

    if dist in distLog.tolist():
        my_index = distLog.tolist().index(dist)
        quantityLog[my_index] += 1
        indexLog[my_index].append(i)

    if dist not in distLog.tolist():
        my_index = distLog.tolist().index([0, 0, 0, 0, 0])
        distLog[my_index] = dist
        quantityLog[my_index] = 1
        indexLog[my_index] = [i]

zero_index = distLog.tolist().index([0, 0, 0, 0, 0])

for i in range(0,zero_index):
    print(str(distLog.tolist()[i]) + " Quantity = " + str(quantityLog.tolist()[i][0]))

#print(indexLog)




