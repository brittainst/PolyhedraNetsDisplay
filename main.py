# when program runs, it will prompt user to enter type of polyhedra net to open, and the
# number of that net (according to the database) to open. it will then draw the net

# todo: nest code in desired nets folder OR import nets to repository

import json  # Allows us to read json files
import numpy as np
from matplotlib import pyplot as plt  # Imports matplotlib so we can plot coordinates

# creates name of the file that needs to be open
name = input("Enter the type of polyhedra:")
number = input("Enter the net number:")
filename = name + 'Net' + str(number) + '.json'

with open(filename) as json_file:  # Calls a particular .json file
    data = json.load(json_file)  # Stores the contents of the database as a list
    v = np.array(data.get("Vertices"))  # Calls database entry as a list and then converts to an array
    e = np.array(data.get("Edges"))  # Calls database entry as a list and then converts to an array
    # x = data.keys() #Stores as a list the names of all the entries in the dictionary.

''' 
Graphnet is a function that takes a list of vertices and edges as an input
and outputs a plot of the net

:args
vlist: array of vertices from data
elist: array of edges from data

'''

def graphnet(vlist, elist):
    w, z = vlist.T  # not really sure what this does
    plt.scatter(w, z)  # plots the vertices

    # For each edge in edge list,
    # Finds the coordinates for each endpoint and plots the line segment
    for x in elist:
        # print(x)
        point1 = vlist[x[0]]
        point2 = vlist[x[1]]
        # print(point1)
        # print(point2)
        x_values = [point1[0], point2[0]]
        y_values = [point1[1], point2[1]]
        plt.plot(x_values, y_values, 'bo', linestyle="-")
    plt.axis('scaled')  # Preserves 1:1 aspect ratio
    plt.show()  # Plots the scatterplot


''' 
radiusg is a function that takes a list of vertices and faces as an input
and outputs the radius of gyration of the net

:args
vlist: array of vertices from data
flist: array of faces from data

'''


def radiusg(vlist, flist):
    # Initializes an array to store the coordinates of the centers of the faces
    FaceCenters = np.zeros((len(flist), 2))
    i = -1  # Starts a counter to keep track of which face is selected

    for face in flist:
        i = i + 1  # updates counter for faces
        centerOfFace = [0, 0] # Initializes an array to store the centers of the faces
        for vertex in face:
            vcoordinates = vlist[vertex] # gets coordinates for each vertex in the face
            centerOfFace = np.add(centerOfFace, vcoordinates) # Adds up values of coordinates

        # Divides by the number of faces to find the coordinates of the center of the face
        centerOfFace[0] = centerOfFace[0] / len(face)
        centerOfFace[1] = centerOfFace[1] / len(face)
        # plt.plot(centerOfFace[0],centerOfFace[1],'bo', linestyle="-")
        FaceCenters[i] = centerOfFace # Stores the coordinates in the array of face centers
    # plt.axis('scaled')
    # plt.show()
    centermass = [0, 0] # Initializes a variable for center of mass
    for center in FaceCenters: # Averages the centers of the faces to find center of mass
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


print(radiusg(v, f))
graphnet(v, e)
# print(f)
