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


def graphnet(vlist, elist, clr, showvertices, linesty):
    if showvertices:
        w, z = vlist.T  # not really sure what this does
        plt.scatter(w, z)  # plots the vertices

    # For each edge in edge list,
    # Finds the coordinates for each endpoint and plots the line segment
    for x in elist:
        point1 = vlist[int(x[0])]
        point2 = vlist[int(x[1])]
        x_values = [point1[0], point2[0]]
        y_values = [point1[1], point2[1]]
        plt.plot(x_values, y_values, color=clr, linestyle=linesty)


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


def countvc(net_type, vlist, elist, scatter):
    target = 0
    numbervc = 0

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
    for i in range(0, len(vlist)):
        deg = 0
        for edge in elist:
            if edge[0] == i:
                deg += 1
            if edge[1] == i:
                deg += 1
        # If the degree matches the target, the number of vertex connections is increased by one
        if deg == target:
            # If user sets scatter TRUE, then adds the coordinates of the vertex connections to a scatter plot
            if scatter:
                plt.scatter(vlist[i][0], vlist[i][1], color='black', s=60)
            numbervc += 1
    return numbervc  # returns the vertex score for that net


'''
degree is a function that takes a vertex and an edge list 
and returns the degree (number of incident edges) of that vertex
'''


def degree(vertex, edge_list):
    deg = 0

    # Calculates the number of incident edges to 'vertex'
    for edge in edge_list:
        if vertex == int(edge[0]):
            deg += 1
        if vertex == int(edge[1]):
            deg += 1
    return deg  # returns the degree of the vertex


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
    return degdistribution


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


'''
function drawnet
'''


def drawnet(name, number):
    filename = name + 'Net' + str(number) + '.json'

    data = loadfile(filename)
    v = np.array(data.get("Vertices"))  # Calls database entry as a list and then converts to an array
    e = np.array(data.get("Edges"))  # Calls database entry as a list and then converts to an array
    x = data.keys()  # Stores as a list the names of all the entries in the dictionary.
    f = np.array(data.get("Faces"))
    facegraph = np.array(data["FaceGraph"]["AdjMat"].get("matrix"))

    # print('Radius of Gyration = ' + str(radiusg(v, f)))
    graphnet(v, e, 'blue', False, '-')  # Plots the net
    vertconnect = str(countvc(name, v, e, True))
    print('Number of Vertex Connections = ' + vertconnect)
    # print('The leaves are ' + str(leaves(name,number)))

    # UNCOMMENT THIS LINE TO PLOT SPANNING TREE OF THE NET
    # graphnet(findcenters(v, f), facegraph, 'red', False)  # plots spanning tree of the net
    centers = findcenters(v, f)
    for i in range(0, len(centers)):
        plt.text(centers[i][0], centers[i][1], str(i), fontsize=12, horizontalalignment='center',
                 verticalalignment='center')

    # print(facegraph)
    firstface = f[0]
    xcoord = 0
    ycoord = 0
    for i in firstface:
        xcoord = xcoord + v[int(firstface[i])][0]
        ycoord = ycoord + v[int(firstface[i])][1]
    xcoord = xcoord / len(firstface)
    ycoord = ycoord / len(firstface)

    # THESE TWO LINES PRINT NETID ON THE NET
    # plt.text(xcoord, ycoord, str(number), fontsize=8, horizontalalignment='center',
    #         verticalalignment='center')

    plt.axis('scaled')  # Preserves 1:1 aspect ratio
    plt.xlabel(name + ' Net ' + str(number) + ': V_c = ' + str(vertconnect))

    FaceCenters = findcenters(v, f)
    centermass = [0, 0]  # Initializes a variable for center of mass
    for center in FaceCenters:  # Averages the centers of the faces to find center of mass
        centermass = np.add(centermass, center)
    centermass[0] = centermass[0] / len(FaceCenters)
    centermass[1] = centermass[1] / len(FaceCenters)

    plt.xlim([centermass[0] - 7, centermass[0] + 7])
    plt.ylim([centermass[1] - 7, centermass[1] + 7])
    # plt.show()  # Plots the scatterplot


def neighbors(face, bindlist):
    list_of_neighbors = []
    for binding in bindlist:
        if binding[0] == face:
            list_of_neighbors.append(binding[1])
        if binding[1] == face:
            list_of_neighbors.append(binding[0])
    return list_of_neighbors


'''
draw_schlegel is a function that draws the schlegel diagram of a dodecahedron
'''


def draw_schlegel(name, number):
    data = loadfile("dodecahedron.json")  # loads file that contains the data of the shape of the Schlegel diagram
    y = data.get("links")  # pulls out the edge information from the file
    z = data.get("nodes")  # pulls out the vertex coordinates information from the file

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
        xsum = 0
        ysum = 0
        for vertex in face:
            xsum += v[vertex][0]
            ysum += v[vertex][1]
        centers_of_faces.append([xsum / 5, ysum / 5])
    # Since the 11th and final face is indicated by the area outside of the Schlegel diagram
    # We append a final coordinate that is placed arbitrary outside the diagram
    centers_of_faces.append([4, 4])

    # Based on user input, filename constructs the name of the file to open.
    filename = name + 'Net' + str(number).zfill(5) + '.json'

    # Loads the information for the Dürer net as data2
    data2 = loadfile(filename)

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
        plt.fill(xlist, ylist, facecolor="#0288d1") # plots and shades the given face

    # when enabled, plots the vertices and edges of the Schlegel diagram
    # graphnet(np.array(v), np.array(e), "blue", True, "-")

    # when enabled, plots a white background under the lines for the cutting tree
    # graphnet(np.array(v), cutting_tree_edge_list, "white", False, "-")

    # plots the cutting tree on the Schlegel diagram
    graphnet(np.array(v), cutting_tree_edge_list, "red", False, "-")

    # Labels the Schlegel Diagram along the x-axis of the plot
    plt.xlabel("Sclegel Diagram" + str(number).zfill(5))

    # when enabled, numbers the vertices on the Schlegel diagram in the original ordering, NOT based on Dürer net
    # for i in range(20):
    #    plt.text(v[i][0], v[i][1], str(i), fontsize=12)

    # scales the axis to preserve geometry
    plt.axis('scaled')
