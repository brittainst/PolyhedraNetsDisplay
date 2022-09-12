from functions import *

#TODO: if name
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

distlog = np.zeros((30, 5)).astype(int)
quantitylog = np.zeros((30,1)).astype(int)
indexlog = [None for i in range(21)]

for i in range(0,numofnets):
    dist = giveDegDist(name, str(i).zfill(k))

    if dist in distlog.tolist():
        my_index = distlog.tolist().index(dist)
        quantitylog[my_index] += 1
        indexlog[my_index].append(i)

    if dist not in distlog.tolist():
        my_index = distlog.tolist().index([0, 0, 0, 0, 0])
        distlog[my_index] = dist
        quantitylog[my_index] = 1
        indexlog[my_index] = [i]

zero_index = distlog.tolist().index([0, 0, 0, 0, 0])

for i in range(0,zero_index):
    print(str(distlog.tolist()[i]) + " Quantity = " + str(quantitylog.tolist()[i][0]))

#print(indexlog)




