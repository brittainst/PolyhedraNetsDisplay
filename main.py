# when program runs, it will prompt user to enter type of polyhedra net to open, and the
# number of that net(according to the database) to open. it will then draw the net

import json  # Allows us to read json files
import numpy as np
from matplotlib import pyplot as plt  # Imports matplotlib so we can plot coordinates

# creates name of the file that needs to be open
name = input("Enter the type of polyhedra:")
number = input("Enter the net number:")
filename = name + str(number) + '.json'

with open(filename) as json_file:  # Calls a particular .json file
    data = json.load(json_file)  # Stores the contents of the database as a list
    v = np.array(data.get("Vertices"))  # Calls database entry as a list and then converts to an array
    e = np.array(data.get("Edges"))  # Calls database entry as a list and then converts to an array
    # x = data.keys() #Stores as a list the names of all the entries in the dictionary.


# graphnet is a function that takes a list of vertices and edges as an input
# and outputs a plot of the net
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


graphnet(v, e)
