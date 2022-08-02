import numpy as np
import math
from matplotlib import pyplot as plt  # Imports matplotlib so we can plot coordinates
import json  # Allows us to read json files


def loadfile(filename):
    with open(filename) as json_file:  # Calls a particular .json file
        data = json.load(json_file)  # Stores the contents of the database as a list
    return data


''' 
Graphnet is a function that takes a list of vertices and edges as an input
and outputs a plot of the net

:args
vlist: array of vertices from data
elist: array of edges from data

'''


def graphnet(vlist, elist, clr, showvertices):
    if showvertices == True:
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

:args
vlist: array of vertices from data
flist: array of faces from data

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

:args
nettype: type of net
vlist: array of vertices from data
elist: array of edges from data

'''


def countvc(nettype, vlist, elist, scatter):
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
            if scatter == True:
                plt.scatter(vlist[i][0], vlist[i][1], color='black', s=60)
            numbervc += 1
    return numbervc


'''
giveDegDist takes a file name and returns the degree distribution of that net

:args
name: net name
number: number of net
'''


def giveDegDist(name, number):
    filename = name + 'Net' + str(number) + '.json'
    data = loadfile(filename)
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

    degdistribution = [0, 0, 0, 0, 0]

    for face in range(0, facequantity):
        deg = 0
        for edge in facegraph:
            if face == int(edge[0]):
                deg += 1
            if face == int(edge[1]):
                deg += 1
        deg = deg / 2
        degdistribution[int(deg) - 1] = degdistribution[int(deg) - 1] + 1
    return (degdistribution)

'''
degree is a function that takes a vertex and an edge list 
and returns the degree (number of incident edges) of that vertex
'''

def degree(v, elist):
    deg = 0
    for e in elist:
        if v == int(e[0]):
            deg += 1
        if v == int(e[1]):
            deg += 1
    return deg

'''
leaves is a function that returns an array of the numbers of which vertices are leaves
'''


def leaves(name, number):
    filename = name + 'Net' + str(number) + '.json'
    data = loadfile(filename)
    facegraph = np.array(data["FaceGraph"]["AdjMat"].get("matrix"))
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

    listofleaves = []

    for face in range(0, facequantity):
        deg = 0
        for edge in facegraph:
            if face == int(edge[0]):
                deg += 1
            if face == int(edge[1]):
                deg += 1
        deg = deg / 2
        if deg == 1:
            listofleaves.append(face)
    return listofleaves



'''
diameter is a function that finds the diameter / longest path across the spanning tree
'''


# TODO: This function not finished yet. I need to go back and write sudo code before finishing
# TODO: Write a function that calculates facequantity based on the type of net
def diameter(name, number):
    filename = name + 'Net' + str(number) + '.json'
    data = loadfile(filename)
    facegraph = np.array(data["FaceGraph"]["AdjMat"].get("matrix"))
    # pulls a list of all the numbers of the leaves in the net
    listofleaves = leaves(name, number)
    # starts an array to track the longest path starting from each leaf
    longestpathsbyvertex = []
    for i in range(0, len(listofleaves - 1)):  # iterates through each leaf except the last one
        pathtracker = [i]  # starts the list with the vertex we are starting with
        for j in range(0, len(pathtracker)):  # iterates through each path in pathtracker
            numadjfound = 0
            for edge in facegraph:
                if int(edge[0]) == i:
                    if numadjfound == 0:
                        pathtracker[j].append(int(edge[1]))
                    else:
                        pathtracker.append(pathtracker[j])
                        pathtracker[len(pathtracker)].append(int(edge[1]))
        longestpathsbyvertex.append(pathtracker)
    return longestpathsbyvertex
