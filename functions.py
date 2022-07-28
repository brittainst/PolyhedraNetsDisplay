import numpy as np
import math
from matplotlib import pyplot as plt  # Imports matplotlib so we can plot coordinates
import json  # Allows us to read json files

def loadfile(shapename, filenumber):
    filename = shapename + str(filenumber) + '.json'
    with open(filename) as json_file:  # Calls a particular .json file
        data = json.load(json_file)  # Stores the contents of the database as a list
    return(data)


''' 
Graphnet is a function that takes a list of vertices and edges as an input
and outputs a plot of the net

:args
vlist: array of vertices from data
elist: array of edges from data

'''
def graphnet(vlist, elist, clr):
    w, z = vlist.T  # not really sure what this does
    plt.scatter(w, z)  # plots the vertices

    # For each edge in edge list,
    # Finds the coordinates for each endpoint and plots the line segment
    for x in elist:
        # print(x)
        point1 = vlist[int(x[0])]
        point2 = vlist[int(x[1])]
        # print(point1)
        # print(point2)
        x_values = [point1[0], point2[0]]
        y_values = [point1[1], point2[1]]
        plt.plot(x_values, y_values, color=clr, linestyle="-")

'''
findcenters is a function that finds the centers of the faces of a net
'''


def findcenters(vlist, flist):
    # Initializes an array to store the coordinates of the centers of the faces
    FaceCenters = np.zeros((len(flist), 2))
    i = -1  # Starts a counter to keep track of which face is selected

    for face in flist:
        i += 1  # updates counter for faces
        centerOfFace = [0, 0]  # Initializes an array to store the centers of the faces
        for vertex in face:
            vcoordinates = vlist[vertex]  # gets coordinates for each vertex in the face
            centerOfFace = np.add(centerOfFace, vcoordinates)  # Adds up values of coordinates

        # Divides by the number of faces to find the coordinates of the center of the face
        centerOfFace[0] = centerOfFace[0] / len(face)
        centerOfFace[1] = centerOfFace[1] / len(face)
        # plt.plot(centerOfFace[0],centerOfFace[1],'bo', linestyle="-")
        FaceCenters[i] = centerOfFace  # Stores the coordinates in the array of face centers
    return (FaceCenters)


''' 
radiusg is a function that takes a list of vertices and faces as an input
and outputs the radius of gyration of the net

:args
vlist: array of vertices from data
flist: array of faces from data

'''


def radiusg(vlist, flist):
    FaceCenters = findcenters(vlist, flist)
    # plt.axis('scaled')
    # plt.show()
    centermass = [0, 0]  # Initializes a variable for center of mass
    for center in FaceCenters:  # Averages the centers of the faces to find center of mass
        centermass = np.add(centermass, center)
    centermass[0] = centermass[0] / len(FaceCenters)
    centermass[1] = centermass[1] / len(FaceCenters)

    # Performs calculation for the value of the radius of gyration
    rgsquared = 0
    for center in FaceCenters:
        x = center[0]
        y = center[1]
        xbar = centermass[0]
        ybar = centermass[1]
        rgsquared = rgsquared + pow(x - xbar, 2) + pow(y - ybar, 2)

    rg = math.sqrt(rgsquared)
    return rg


'''
countvc is a function that counts vertex connections
'''


def countvc(nettype, vlist, elist):
    target = 0
    numbervc = 0
    if nettype == 'Dodecahedron':
        target = 4
    elif nettype == 'Icosahedron':
        target = 6
    elif nettype == 'Octahedron':
        target = 5
    else:
        target = 4
    for i in range(0, len(vlist)):
        counter = 0
        for edge in elist:
            if edge[0] == i:
                counter += 1
            if edge[1] == i:
                counter += 1
        if counter == target:
            plt.scatter(vlist[i][0], vlist[i][1], color='black', s=120)
            numbervc += 1
    return numbervc

'''
giveDegDist takes a file name a returns the degree distribution of that net
'''

def giveDegDist(name, number):
    data=loadfile(name,number)
    facegraph = np.array(data["FaceGraph"]["AdjMat"].get("matrix"))

    facequantity = 0
    if name == 'Tetrahedron':
        facequantity = 4
    elif name == 'Cube':
        facequantity = 6
    elif name == 'Octahedron':
        facequantity = 8
    elif name == 'Dodecahedron':
        facequantity = 12
    else:
        facequantity = 20

    degdistribution = [0,0,0,0,0]

    for face in range(0, facequantity):
        deg = 0
        for edge in facegraph:
            if face == int(edge[0]):
                deg += 1
            if face == int(edge[1]):
                deg += 1
        deg = deg/2
        degdistribution[int(deg)-1] = degdistribution[int(deg)-1] + 1
    return(degdistribution)