import numpy as np
import math
from matplotlib import pyplot as plt  # Imports matplotlib so we can plot coordinates
import json  # Allows us to read json files
from matplotlib.figure import Figure
from tkinter import *
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def concat_length(string):
    z = -1
    if string == "Tetrahedron":
        z = 1
    elif string == "Cube" or string == "Octahedron":
        z = 2
    elif string == "Dodecahedron" or string == "Icosahedron":
        z = 5
    if z == -1:
        print("Spelling Error")
    if z > 0:
        return z

def num_of_nets(string):
    z = -1
    if string == "Tetrahedron":
        z = 2
    elif string == "Cube" or string == "Octahedron":
        z = 11
    elif string == "Dodecahedron" or string == "Icosahedron":
        z = 43380
    if z == -1:
        print("Spelling Error")
    if z > 0:
        return z


def loadFile(name, number):
    filename = name + 'Net' + str(number) + '.json'  # Some functions already input number as string, but others do not
    with open(filename) as json_file:  # Calls a particular .json file
        data = json.load(json_file)  # Stores the contents of the database as a list
    return data


''' 
Graphnet is a function that takes a list of vertices and edges as an input
and outputs a plot of the net
(SEE DRAWNET: graphnet is mainly used in other functions, drawnet draws more complex graphs)

:args
vlist: array of vertices from data
elist: array of edges from data
clr: The color to plot the data as
showvertices: Boolean to determine whether to plot the vertices and the edges, or just show the edges
linesty: Allows the user to enter a string to dictate the linestyle, i.e. solid edges, dashed edges, etcetera
'''


def graphNet(vList, eList, clr, alphaval, showVertices, lineSty):
    if showVertices:
        w, z = vList.T  # not really sure what this does
        plt.scatter(w, z, alpha=1)  # plots the vertices

    # For each edge in edge list,
    # Finds the coordinates for each endpoint and plots the line segment
    for x in eList:
        point1 = vList[int(x[0])]
        point2 = vList[int(x[1])]
        x_values = [point1[0], point2[0]]
        y_values = [point1[1], point2[1]]
        plt.plot(x_values, y_values, color=clr, alpha=alphaval, linestyle=lineSty)

'''
findcenters is a function that finds the centers of the faces of a net

:args
vlist: array of vertices from data
flist: array of faces from data

'''


def findCenters(vList, fList):
    # Initializes an array to store the coordinates of the centers of the faces
    faceCenters = np.zeros((len(fList), 2))
    i = -1  # Starts a counter to keep track of which face is selected

    for face in fList:
        i += 1  # updates counter for faces
        center_of_face = [0, 0]  # Initializes an array to store the centers of the faces
        for vertex in face:
            vCoordinates = vList[vertex]  # gets coordinates for each vertex in the face
            center_of_face = np.add(center_of_face, vCoordinates)  # Adds up values of coordinates

        # Divides by the number of faces to find the coordinates of the center of the face
        center_of_face[0] = center_of_face[0] / len(face)
        center_of_face[1] = center_of_face[1] / len(face)
        faceCenters[i] = center_of_face  # Stores the coordinates in the array of face centers
    return (faceCenters)


''' 
radiusg is a function that takes a list of vertices and faces as an input
and outputs the radius of gyration of the net

:args
vlist: array of vertices from data
flist: array of faces from data

'''


def radius_of_gyration(vList, fList):
    FaceCenters = findCenters(vList, fList)
    centerMass = [0, 0]  # Initializes a variable for center of mass
    for center in FaceCenters:  # Averages the centers of the faces to find center of mass
        centerMass = np.add(centerMass, center)
    centerMass[0] = centerMass[0] / len(FaceCenters)
    centerMass[1] = centerMass[1] / len(FaceCenters)

    # Performs calculation for the value of the radius of gyration
    rgsquared = 0
    for center in FaceCenters:
        x = center[0]
        y = center[1]
        xBar = centerMass[0]
        yBar = centerMass[1]
        rgsquared = rgsquared + pow(x - xBar, 2) + pow(y - yBar, 2)

    # Takes the square root to find the actual value of the radius of gyration
    rg = math.sqrt(rgsquared)
    return rg


'''
countvc is a function that counts vertex connections

:args
nettype: type of net
vlist: array of vertices from data
elist: array of edges from data
scatter: scatter is a boolean that indicates whether or not to try and plot the vertex connections on the graph

'''


def countVC(net_type, vList, eList, scatter):
    target = 0
    numberVC = 0

    # TODO: change to switch function
    # takes user input to determine the degree needed to be a vertex connection
    if net_type == 'Tetrahedron':
        target = 4
    elif net_type == 'Cube':
        target = 4
    elif net_type == 'Octahedron':
        target = 5
    elif net_type == 'Dodecahedron':
        target = 4
    elif net_type == 'Icosahedron':
        target = 6

    # for each vertex of the graph, determines the degree of that vertex
    for i in range(0, len(vList)):
        deg = 0
        for edge in eList:
            if edge[0] == i:
                deg += 1
            if edge[1] == i:
                deg += 1
        # If the degree matches the target, the number of vertex connections is increased by one
        if deg == target:
            # If user sets scatter TRUE, then adds the coordinates of the vertex connections to a scatter plot
            if scatter:
                plt.scatter(vList[i][0], vList[i][1], color='black', s=60)
            numberVC += 1
    return numberVC  # returns the vertex score for that net


'''
degree is a function that takes a vertex and an edge list 
and returns the degree (number of incident edges) of that vertex
'''


def degree(vertex, edge_list):
    deg = 0

    # Calculates the number of incident edges to 'vertex'
    for edge in edge_list:
        # TODO: shorten if statement to if or
        if vertex == int(edge[0]) or vertex == int(edge[1]):
            deg += 1
        # if vertex == int(edge[1]):
          #  deg += 1
    return deg  # returns the degree of the vertex


'''
giveDegDist takes a file name and returns the degree distribution of that net

:args
name: net name
number: number of net
'''


def giveDegDist(name, number):
    data = loadFile(name, number)

    # facegraph stores the data of which face is adjacent to which
    # TODO: find duplicates
    faceGraph = np.array(data["FaceGraph"]["AdjMat"].get("matrix"))

    # gives the number of faces the Dürer net has based on what type of net it is
    if name == 'Tetrahedron':
        faceQuantity = 4
    elif name == 'Cube':
        faceQuantity = 6
    elif name == 'Octahedron':
        faceQuantity = 8
    elif name == 'Dodecahedron':
        faceQuantity = 12
    else:
        faceQuantity = 20
        # TODO: something above is funky (switch, add exception) (end of duplicates)

    # initializes an array to track how many vertices of each degree there are on the spanning tree
    # The ith entry stores the number of vertices of degree i + 1
    degDistribution = [0, 0, 0, 0, 0]

    # Calculates the degree of each face in the net and adds 1 to the appropriate entry in degdistribution
    for face in range(0, faceQuantity):
        deg = 0
        for edge in faceGraph:
            if face == int(edge[0]):
                deg += 1
            if face == int(edge[1]):
                deg += 1
        deg = deg / 2
        degDistribution[int(deg) - 1] = degDistribution[int(deg) - 1] + 1
    return degDistribution


'''
leaves is a function that returns an array of the numbers of which vertices are leaves
'''


def leaves(name, number):
    data = loadFile(name, number)
    faceGraph = np.array(data["FaceGraph"]["AdjMat"].get("matrix"))
    if name == 'Tetrahedron':
        faceQuantity = 4
    elif name == 'Cube':
        faceQuantity = 6
    elif name == 'Octahedron':
        faceQuantity = 8
    elif name == 'Dodecahedron':
        faceQuantity = 12
    else:
        faceQuantity = 20

    listOfLeaves = []

    for face in range(0, faceQuantity):
        deg = 0
        for edge in faceGraph:
            if face == int(edge[0]):
                deg += 1
            if face == int(edge[1]):
                deg += 1
        deg = deg / 2
        if deg == 1:
            listOfLeaves.append(face)
    return listOfLeaves


'''
diameter is a function that finds the diameter / longest path across the spanning tree
'''


# TODO: This function not finished yet. I need to go back and write sudo code before finishing
# TODO: Write a function that calculates facequantity based on the type of net
def diameter(name, number):
    data = loadFile(name, number)
    faceGraph = np.array(data["FaceGraph"]["AdjMat"].get("matrix"))
    # pulls a list of all the numbers of the leaves in the net
    listOfLeaves = leaves(name, number)
    # starts an array to track the longest path starting from each leaf
    longestPathsByVertex = []
    for i in range(0, len(listOfLeaves) - 1):  # iterates through each leaf except the last one
        pathTracker = [i]  # starts the list with the vertex we are starting with
        for j in range(0, len(pathTracker)):  # iterates through each path in pathtracker
            numAdjFound = 0
            for edge in faceGraph:
                if int(edge[0]) == i:
                    if numAdjFound == 0:
                        pathTracker[j].append(int(edge[1]))
                    else:
                        pathTracker.append(pathTracker[j])
                        pathTracker[len(pathTracker)].append(int(edge[1]))
        longestPathsByVertex.append(pathTracker)
    return longestPathsByVertex


'''
drawnet is a function that graphs visual representations of Dürer net. It does slightly more than graphnet.
graphnet just plots a graph given an vertex list and an edge list.
drawnet encorporates other functions to add more data to the graph, like drawing the spanning tree, 
convex hull, or numbering the faces
'''


def drawNet(name, number, numberfaces=False, vc=False, showVertices=False, spanning=False):
    # calls the appropriate file from the database and stores it as the dictionary data
    data = loadFile(name, number)

    # Pulls out information from data and stores it as separate arrays.
    # v holds vertex information, e holds edge information, f holds face information,
    # and faceGraph holds information about which face is next to which face in the Dürer net
    v = np.array(data.get("Vertices"))
    e = np.array(data.get("Edges"))
    x = data.keys()
    f = np.array(data.get("Faces"))

    # this variable is only used in lines of code that are manually commented & uncommented out
    faceGraph = np.array(data["FaceGraph"]["AdjMat"].get("matrix"))

    # when enabled prints the radius of gyration of the Dürer net
    # print('Radius of Gyration = ' + str(radiusg(v, f)))

    # plots the Dürer net in black, only plots the edges, and uses a solid '-' line
    graphNet(v, e, 'blue', 1, showVertices, '-')

    # stores the number of vertex connections as vertConnect
    # The boolean set to True also tells it to add those vertex connections to the plot
    if vc== True:
        vertConnect = str(countVC(name, v, e, True))

        # prints the number of vertex connections
        # print('Number of Vertex Connections = ' + vertConnect)

    # When enabled prints what the leaves are
    # print('The leaves are ' + str(leaves(name,number)))

    # UNCOMMENT THIS LINE TO PLOT SPANNING TREE OF THE NET
    if spanning:
        graphNet(findCenters(v, f), faceGraph, 'red', 1, False, '-')  # plots spanning tree of the net

    # numbers the faces of the graph
    centers = findCenters(v, f)  # finds the center of each face
    if numberfaces:
        for i in range(0, len(centers)):  # for each face, plots the number of the face on the faces center
            plt.text(centers[i][0], centers[i][1], str(i), fontsize=12, horizontalalignment='center',
                 verticalalignment='center')

    # when enabled these three lines print the number of the net on the center of the 0th face
    # xCoord = centers[0][0]
    # yCoord = centers[0][1]
    # plt.text(xCoord, yCoord, str(number), fontsize=8, horizontalalignment='center', verticalalignment='center')

    plt.axis('scaled')  # Preserves 1:1 aspect ratio
    if vc==True:
        plt.xlabel(name + ' Net ' + str(number) + ': V_c = ' + str(vertConnect))  # labels x axis
    else:
        plt.xlabel(name + 'Net' + str(number))

    # the next few lines finds the center of mass of the Dürer net
    centermass = [0, 0]  # Initializes a variable for center of mass
    for center in centers:  # Averages the centers of the faces to find center of mass
        centermass = np.add(centermass, center)
    centermass[0] = centermass[0] / len(centers)
    centermass[1] = centermass[1] / len(centers)

    if numberfaces:
        # Adds the center of mass of the net to the plot
        plt.scatter([centermass[0]], [centermass[1]], color='red', s=60)

    # sets the scale of the plot based on the center of mass of the center of mass of the net.
    plt.xlim([centermass[0] - 7, centermass[0] + 7])
    plt.ylim([centermass[1] - 7, centermass[1] + 7])


'''
neighbors takes a list of faces and a list of which faces are bound to which other faces and returns
the list_of_neighbors. That is the list of neighboring faces of the original face
NOTE TO SELF: This should apply to any graph with vertices and edges. If passed a vertex list and an edge list,
effectively this would return the neighboring vertices of the original vertex.
'''


def neighbors(face, bindList):
    list_of_neighbors = []
    for binding in bindList:
        if binding[0] == face:
            list_of_neighbors.append(binding[1])
        if binding[1] == face:
            list_of_neighbors.append(binding[0])
    return list_of_neighbors


'''
draw_schlegel is a function that draws the schlegel diagram of a dodecahedron
'''


# TODO: there's gotta be a better way to do some of this but idk exactly what yet
def draw_schlegel(name, number):

    # THESE THREE LINES CANNOT BE OPTIMIZED WITH THE LOADFILE FUNCTION
    filename = 'dodecahedron.json'
    with open(filename) as json_file:  # Calls a particular .json file
        data = json.load(json_file)  # Stores the contents of the database as a list

    y = data.get("links")  # pulls out the edge information from the file
    z = data.get("nodes")  # pulls out the vertex coordinates information from the file
    print(y)
    # Takes the edge information and restores it in a more desirable format
    e = []
    for i in range(30):
        e.append([y[i]["source"], y[i]["target"]])

    # Takes the vertex information and restores it in a more desirable format
    v = []
    for i in range(20):
        v.append([z[i]["x"], z[i]["y"]])

    # internal_faces is a 2D array where the ith entry is a list of the vertices that make up that face on the
    # Schlegel diagram
    internal_faces = [[0, 1, 2, 3, 19],
                      [1, 2, 6, 7, 8],
                      [2, 3, 4, 5, 6],
                      [3, 4, 17, 18, 19],
                      [0, 10, 11, 18, 19],
                      [0, 1, 8, 9, 10],
                      [5, 6, 7, 14, 15],
                      [7, 8, 9, 13, 14],
                      [9, 10, 11, 12, 13],
                      [11, 12, 16, 17, 18],
                      [4, 5, 15, 16, 17]]

    # Calculates the coordinates of the center of each face on the Schlegel diagram
    # This tells us where to place the number on each face
    centers_of_faces = []
    for face in internal_faces:
        xSum = 0
        ySum = 0
        for vertex in face:
            xSum += v[vertex][0]
            ySum += v[vertex][1]
        centers_of_faces.append([xSum / 5, ySum / 5])
    # Since the 11th and final face is indicated by the area outside of the Schlegel diagram
    # We append a final coordinate that is placed arbitrary outside the diagram
    centers_of_faces.append([4, 4])

    # Loads the information for the Dürer net as data2
    data2 = loadFile(name, str(number).zfill(5))

    f = np.array(data2.get("Faces"))  # Stores face information for the Dürer net
    durer_edges = np.array(data2.get("Edges"))  # Stores edge information for the Dürer net
    durer_gluing = np.array(data2.get("Gluing"))  # Store gluing information for the Dürer net

    # Stores information about Dihedral Angles
    # More importantly, incidentally stores data on which faces will be adjacent to which faces
    # in the completed Dodecahedron
    g = np.array(data2.get("DihedralAngles"))

    # extracts info on which face will be adjacent to which and stores it as a 2D array called face_bindings
    face_bindings = []
    for i in range(30):
        face_bindings.append([g[i]["Face-0"], g[i]["Face-1"]])

    # face_ordering is a renumbering of the faces of the Schlegel diagram so that they match the faces of the Dürer net
    # The order in which we must find the faces is the order that is inherent from the 2D array internal_faces
    face_ordering = [0]  # initiates this list with face 0 being 0
    # chooses the next face to be any face that shares an edge with face 0
    for i in range(12):
        found = False
        if i not in face_ordering:  # for each number not already chosen
            for binding in face_bindings:  # looks through face_bindings for a face that will be adjacent to face 0
                if binding[0] == 0:
                    face_ordering.append(binding[1])
                    found = True
                if binding[1] == 0:
                    face_ordering.append(binding[0])
                    found = True
                if found:
                    break
                # when a match is found, adds the new face to face_ordering and exits for loops
        if found:
            break
    # finds face 2 by searching for a face, not already listed, adjacent to faces 0 and 1
    # There are two options for face 2, but orientation does not matter, so it selects which ever one it finds first
    # and then breaks the for loop
    for i in range(12):
        if i not in face_ordering:
            list_of_neighbors = neighbors(i, face_bindings)  # finds all neighbors of i
            # if i is neighbors with both faces 0 and 1, face i is appended and for loops is terminated
            if face_ordering[0] in list_of_neighbors and face_ordering[1] in list_of_neighbors:
                face_ordering.append(i)
                break
    # the next 8 for loops follow similar logic to the previous one, finding the face that is adjacent to the
    # appropriate 2 proceeding ones, based on inherit ordering of the faces on the Schlegel diagram and appends
    # it accordingly.
    # finds face 3
    for i in range(12):
        if i not in face_ordering:
            list_of_neighbors = neighbors(i, face_bindings)
            if face_ordering[0] in list_of_neighbors and face_ordering[2] in list_of_neighbors:
                face_ordering.append(i)
                break
    # finds face 4
    for i in range(12):
        if i not in face_ordering:
            list_of_neighbors = neighbors(i, face_bindings)
            if face_ordering[0] in list_of_neighbors and face_ordering[3] in list_of_neighbors:
                face_ordering.append(i)
                break
    # finds face 5
    for i in range(12):
        if i not in face_ordering:
            list_of_neighbors = neighbors(i, face_bindings)
            if face_ordering[0] in list_of_neighbors and face_ordering[4] in list_of_neighbors:
                face_ordering.append(i)
                break
    # finds face 6
    for i in range(12):
        if i not in face_ordering:
            list_of_neighbors = neighbors(i, face_bindings)
            if face_ordering[1] in list_of_neighbors and face_ordering[2] in list_of_neighbors:
                face_ordering.append(i)
                break
    # finds face 7
    for i in range(12):
        if i not in face_ordering:
            list_of_neighbors = neighbors(i, face_bindings)
            if face_ordering[1] in list_of_neighbors and face_ordering[5] in list_of_neighbors:
                face_ordering.append(i)
                break
    # finds face 8
    for i in range(12):
        if i not in face_ordering:
            list_of_neighbors = neighbors(i, face_bindings)
            if face_ordering[4] in list_of_neighbors and face_ordering[5] in list_of_neighbors:
                face_ordering.append(i)
                break
    # finds face 9
    for i in range(12):
        if i not in face_ordering:
            list_of_neighbors = neighbors(i, face_bindings)
            if face_ordering[3] in list_of_neighbors and face_ordering[4] in list_of_neighbors:
                face_ordering.append(i)
                break
    # finds face 10
    for i in range(12):
        if i not in face_ordering:
            list_of_neighbors = neighbors(i, face_bindings)
            if face_ordering[2] in list_of_neighbors and face_ordering[3] in list_of_neighbors:
                face_ordering.append(i)
                break
    # finds face 11 by appending the only face that hasn't been selected yet
    for i in range(12):
        if i not in face_ordering:
            face_ordering.append(i)

    # numbers the faces on the schlegel diagram by placing the correct number on the center of the ith face
    for i in range(12):
        plt.text(centers_of_faces[i][0], centers_of_faces[i][1], str(face_ordering[i]), fontsize=12,
                 horizontalalignment='center',
                 verticalalignment='center')

    # cutting_tree will store tuples of faces that are cut between in the unfolding of the Dodecahedron
    cutting_tree = []

    # iterates through all edges of the Dürer net
    for i in range(len(durer_edges)):
        # counts how many faces the edge i lies along
        numf = 0
        for face in f:
            if durer_edges[i][0] in face and durer_edges[i][1] in face:
                numf += 1
        # we proceed only if the number of faces is 1, as that means it is an edge that will be glued to another
        if numf == 1:
            edge_glued_to = 0  # initiates a variable to store which edge the edge i gets glued to
            # finds the edge that the edge i is glued to and stores it as edge_glued_to
            for glue in durer_gluing:
                if glue[0] == i:
                    edge_glued_to = glue[1]
                elif glue[1] == i:
                    edge_glued_to = glue[0]
            face1 = 0
            face2 = 0
            # finds which face our edge i lies on and stores it as face1
            for j in range(len(f)):
                if durer_edges[i][0] in f[j] and durer_edges[i][1] in f[j]:
                    face1 = j
            # finds which face our edge_glued_to lies on and stores it as face2
            for j in range(len(f)):
                if durer_edges[edge_glued_to][0] in f[j] and durer_edges[edge_glued_to][1] in f[j]:
                    face2 = j
            # adds this pair of edges that are cut between to the array cutting_tree
            cutting_tree.append([face1, face2])

    # a new array to store a translation of the data in cutting_tree
    # new_array will be a list of which two faces need to be cut between on the Schlegel diagram
    # according to the original number of the faces on the Schlegel diagram
    new_array = []

    # cutting_tree_edge_list will track the ACTUAL edges the cutting tree is made up of
    cutting_tree_edge_list = []

    # for each pair of faces in cutting_tree, finds what numbers those faces would be in the original ordering
    # and stores that pair with the new (original) numbers to new_array
    for face_pair in cutting_tree:
        internal_face1 = 0
        internal_face2 = 0
        for index in range(len(face_ordering)):
            if face_ordering[index] == face_pair[0]:
                internal_face1 = index
            if face_ordering[index] == face_pair[1]:
                internal_face2 = index
        new_array.append([internal_face1, internal_face2])

    # adds the 12th exterior face that we haven't needed before, but will need for finding the edges of the cutting tree
    internal_faces.append([12, 13, 14, 15, 16])

    # for each pair of faces that will be cut between, finds the edge that they share
    # and adds it to cutting_tree_edge_list
    for face_pair in new_array:
        shared_edge = []
        for i in internal_faces[face_pair[0]]:
            if i in internal_faces[face_pair[1]]:
                shared_edge.append(i)
        cutting_tree_edge_list.append(shared_edge)

    # THIS BEGINS VISUAL REPRESENTATION OF THE PREVIOUS CALCUlATIONS

    # for each interior face (does not include the last exterior face)
    # finds a boundary slightly interior to the faces true boundary and shades it in
    for face in range(len(internal_faces) - 1):  # iterates for every interior face of the Schlegel diagram
        xlist = []
        ylist = []
        for vertex in internal_faces[face]:  # for each vertex of the currently selected face
            x1 = v[vertex][0]  # pulls x and y coordinates of that vertex
            y1 = v[vertex][1]
            x2 = centers_of_faces[face][0]  # pulls the previously calculated coordinates for the center of that face
            y2 = centers_of_faces[face][1]
            x3 = 0.9 * x1 + 0.1 * x2  # weights the points 10% of the way to center of that face
            y3 = 0.9 * y1 + 0.1 * y2  # so that the shading stops just before the edge of the face
            xlist.append(x3)
            ylist.append(y3)
        plt.fill(xlist, ylist, facecolor="#0288d1")  # plots and shades the given face

    # when enabled, plots the vertices and edges of the Schlegel diagram
    # graphNet(np.array(v), np.array(e), "blue", True, "-")

    # when enabled, plots a white background under the lines for the cutting tree
    # graphNet(np.array(v), cutting_tree_edge_list, "white", False, "-")

    # plots the cutting tree on the Schlegel diagram
    graphNet(np.array(v), cutting_tree_edge_list, "red", False, "-")

    # Labels the Schlegel Diagram along the x-axis of the plot
    plt.xlabel("Sclegel Diagram" + str(number).zfill(5))

    # when enabled, numbers the vertices on the Schlegel diagram in the original ordering, NOT based on Dürer net
    # for i in range(20):
    #    plt.text(v[i][0], v[i][1], str(i), fontsize=12)

    # scales the axis to preserve geometry
    plt.axis('scaled')


'''
center_of_mass is a function that returns the center of mass of a list of points
'''

#TODO: find places where this function should be implemented and isn't
def center_of_mass(points):
    # sets initial values for the x and y coordinates of the center of mass
    cmx = 0
    cmy = 0
    for point in points:  # for each point in the list of points, tallies up the sum of coordinates
        cmx += point[0]
        cmy += point[1]
    cmx = cmx / len(points)  # Divides sum of coordinates to find the actual center of mass
    cmy = cmy / len(points)
    return [cmx, cmy]  # Returns the center of mass


'''
dist a function that returns the distance between two points
'''


def distance(point1, point2):  # Finds the distance between two points
    x_1 = point1[0]  # stores x coordinate of first point
    y_1 = point1[1]  # stores y coordinate of first point
    x_2 = point2[0]  # stores x coordinate of second point
    y_2 = point2[1]  # stores y coordinate of second point
    dSquared = math.pow(x_1 - x_2, 2) + math.pow(y_1 - y_2, 2)  # distance formula for d^2
    d = math.sqrt(dSquared)  # takes square root to find distance
    return d  # returns distance


'''
radius_bounding_circle finds the radius of the bounding circle of a net
'''


def radius_bounding_circle(name, number, plot):
    data = loadFile(name, number)  # Stores net information as a dictionary
    v = np.array(data.get("Vertices"))  # Loads vertices of the net
    f = np.array(data.get("Faces"))  # Loads faces of the net
    centers = findCenters(v, f)  # stores the centers of each face of the net
    cent_mass = center_of_mass(centers)  # finds center of mass of the net
    distances = []  # an array to store how far each vertex of the durer net is from the center of the net
    for vertex in v:
        distances.append(distance(vertex, cent_mass))
    radius = max(distances)

    if plot:
        fig = plt.gcf()
        ax = fig.gca()
        ax.add_patch(plt.Circle(cent_mass, radius, fill=False))

    return radius


'''
bounding_circle_2 stricter bounding circle
'''


def bounding_circle_2(name, number, plot):
    data = loadFile(name, number)  # Stores net information as a dictionary
    v = np.array(data.get("Vertices"))  # Loads vertices of the net
    dm = 0
    point1 = []
    point2 = []
    for vertex in v:
        for vertex2 in v:
            temp = distance(vertex, vertex2)
            if temp > dm:
                point1 = vertex
                point2 = vertex2
                dm = temp
    radius = dm / 2

    if plot:
        fig = plt.gcf()
        ax = fig.gca()
        center = [point1[0] / 2 + point2[0] / 2, point1[1] / 2 + point2[1] / 2]
        ax.add_patch(plt.Circle(center, radius, fill=False))
    return radius


'''
angle is a function that finds the angle formed by 3 points
'''


def angle(p1, p2, p3):
    # First thing is to center p2 at the origin and then recalculate the coordinates of p1
    x1 = p1[0] - p2[0]  # x coordinate of first point with p2 centered at origin
    y1 = p1[1] - p2[1]  # y coordinate of first point with p2 centered at origin
    x2 = p3[0] - p2[0]  # x coordinate of second point with ...
    y2 = p3[1] - p2[1]  # y coordinate of second point ...

    # Uses arctan function to calculate angle of inclination of line from origin to point 2
    theta1 = np.arctan2(y2, x2) * 180 / math.pi
    # Uses arctan function to calculate angle of inclination of line from origin to point 1
    theta2 = np.arctan2(y1, x1) * 180 / math.pi

    # If the output is negative, does 360 - output to get the positive version of the angle
    if theta1 < 0:
        theta1 += 360
    if theta2 < 0:
        theta2 += 360

    theta = theta1 - theta2  # subtracts two angles to get the angle inbetween the lines
    return theta  # returns the angle


'''
generate_angles is a function that takes a list of coordinates and finds the exterior angles of each
set of three points using the angle function.
'''


def generate_angles(points):
    # Starts with an empty array for angles
    angles = []

    # for each point in the list of points, we take the vertex on either side and calculate the angle between the 3 pnts
    for i in range(1, len(points)):
        measure = angle(points[i - 2], points[i - 1], points[i])  # finds angle
        angles.append(measure)  # appends to list of angles
    angles.append(angle(points[-2], points[-1], points[0]))  # appends angle for last set of coordinates in list points

    # TODO: check this loop
    # Checks that the angles are positive, and if negative does 360 - output to make them positive
    # This might be redundant but I'm not sure
    for i in range(len(angles)):
        if angles[i] < 0:
            angles[i] += 360
        # Rounds angles to 2 degrees to try to get rid of variation in calculations caused by rounding
        angles[i] = round(angles[i], 2)
    return angles  # returns list of angles


'''
convex_hull is a function that finds the convex hull of a Dürer net
'''


# TODO: has code used in a lot of places. can probably add a function and shorten abt 100 lines throughout this file
#  (the part storing vertices, edges, faces)
def convex_hull(name, number, plot):
    data = loadFile(name, number)  # Stores net information as a dictionary
    v = np.array(data.get("Vertices"))  # stores vertices of Dürer net
    durer_edges = np.array(data.get("Edges"))  # stores edges of Dürer net
    f = np.array(data.get("Faces"))  # stores faces of Dürer net

    # edges is a new array to hold the edges that make up the outer boundary of the Dürer net
    edges = []

    # for each edge of the Dürer net, take the ones that are only adjacent to one face (i.e. the ones on the
    # outside of the net that make up the boundary) and append them to the list edges
    for i in range(len(durer_edges)):  # for each edge of the Dürer net
        numf = 0
        for face in f:  # for each face of the net
            # If both the vertices of the edge are part of that face
            if durer_edges[i][0] in face and durer_edges[i][1] in face:
                # increase the number of faces it lies on by 1
                numf += 1
        # we proceed only if the number of faces is 1, as that means it is an edge that will be glued to another
        if numf == 1:
            edges.append(durer_edges[i])  # append the edge to the list of edges that make up the boundary.

    # new_vertex_order will store the order of the vertices as we go around the outside of the Dürer net
    new_vertex_order = [0]

    # Determines z: the number of edges on that type of Dürer net
    # and determines bound: the maximum angle we wish to allow for that type of Dürer net
    if name == "Cube":
        z = 14
        bound = 280
    elif name == "Octahedron":
        z = 10
        bound = 310
    elif name == "Dodecahedron":
        z = 38
        bound = 262
    elif name == "Icosahedron":
        z = 22
        bound = 310

    # THIS FOR LOOP IS WHAT WAS CAUSING THE ISSUE OF MEASURING INTERIOR ANGLES INSTEAD OF EXTERIOR ANGLES
    # Since I course corrected this mistake elsewhere in the code, this doesn't need to be changed for now
    # This for loop builds the new vertex order by taking the last vertex and finding the edge along the boundary
    # that includes it, and another vertex that is not already in the new vertex order. Then it appends that
    # new vertex to the vertex order.

    # TODO: fix the interior/exterior error (even if it works as is!)

    for i in range(1, z):
        for edge in edges:
            if new_vertex_order[i - 1] == edge[0] and edge[1] not in new_vertex_order:
                new_vertex_order.append(edge[1])
                break
            if new_vertex_order[i - 1] == edge[1] and edge[0] not in new_vertex_order:
                new_vertex_order.append(edge[0])
                break

    # Creates a new list of vertex connections in the order that they occur going around the outside of the Dürer net
    reordered_vertex_coordinates = [[0, 0] for i in range(38)]
    for i in range(len(new_vertex_order)):
        reordered_vertex_coordinates[i] = v[new_vertex_order[i]]

    # Uses the new order of the vertex connections to calculate the exterior angles of the polygon they define
    angles = generate_angles(reordered_vertex_coordinates)
    # We need to check if it has recorded the internal or external angles
    # We do this using the compare string
    string = data.get("CmpString")
    marker = False

    # TODO: add switch

    # The first entry in the compare string tells us what the first angle in our list angles should be
    if string[0] == "A":
        desired_angle = 252.
    if string[0] == "B":
        desired_angle = 144.
    if string[0] == "C":
        desired_angle = 36.

    # If the first angle is not within a reasonable bound of what we determine it should be.
    # We set marker = True, which tells our code later to flip the angles from interior angles to exterior angles
    if angles[0] < desired_angle - 1 or angles[0] > desired_angle + 1:
        marker = True
        # We also flip the angles from the first calculation to start
        for i in range(len(angles)):
            angles[i] = 360 - angles[i]

    # This for loop is set to go an arbitrary amount of times that is more than enough to finish the process
    for j in range(35):
        for i in range(len(angles)):
            # Each time through we search for an exterior angle that is less than 180 degrees
            if angles[i] < 180 or angles[i] > bound:
                # If we find one we delete it from both the coordinates list and the vertex order list
                # and we break the for loop
                reordered_vertex_coordinates = np.delete(reordered_vertex_coordinates, i, 0)
                new_vertex_order = np.delete(new_vertex_order, i)
                break
        # We then recalculate the angles of the new polygon formed with this vertex removed.
        angles = generate_angles(reordered_vertex_coordinates)

        # If we found that we were measuring interior angles instead of exterior angles before, we flip them
        # to be exterior angles every time we recalculate the angles.
        if marker:
            for i in range(len(angles)):
                angles[i] = 360 - angles[i]

    # We now want to find the edges that make up the convex hull
    # HULL_EDGES AND THE FOLLOWING FOR LOOP ARE NOT NEEDED FOR CALCULATING AREA
    # THEY ARE ONLY NEEDED FOR CALLING GRAPHNET TO ADD THE CONVEX HULL TO THE PLOT
    # TODO: move this, possibly
    hull_edges = []

    # once the process of deleting vertices is finished
    # For each pair of vertices that are next to each other in the list
    # we add an edge consisting of those 2 vertices to hull_edges
    for i in range(len(new_vertex_order)):
        hull_edges.append([new_vertex_order[i - 1], new_vertex_order[i]])

    # The following uses Heron's formula for finding the area of a triangle
    area = 0
    for i in range(len(new_vertex_order)):
        p1 = reordered_vertex_coordinates[i - 1]
        p2 = reordered_vertex_coordinates[i]
        a = distance([0, 0], p1)
        b = distance([0, 0], p2)
        c = distance(p1, p2)
        s = (a + b + c) / 2
        A = math.sqrt(s * (s - a) * (s - b) * (s - c))
        area += A

    # We calculate the perimeter by just adding the distance between each pair of adjacent vertices
    # using the dist() function defined earlier
    perimeter = 0
    for i in range(len(reordered_vertex_coordinates)):
        perimeter += distance(reordered_vertex_coordinates[i - 1], reordered_vertex_coordinates[i])

    # If variable plot is True, plots the convex hull
    if plot:
        graphNet(v, np.array(hull_edges), "red", False, "-")

    # Returns [area of the convex hull, perimeter of the convex hull
    return [area, perimeter]


'''
generate_perimeter_list generates the length of the perimeter of the convex hull for every Dodecahedron Dürer net
and returns those values as a list/array
'''


def generate_perimeter_list():
    perimeter_list = []
    for i in range(0, 43380):
        # convex_hull returns [ area of convex hull, perimeter of convex hull ]
        # So the [1] at the end of the line is pulling out the perimeter, and then we are appending it to the list
        perimeter_list.append(convex_hull("Dodecahedron", str(i).zfill(5), False)[1])

    return perimeter_list

