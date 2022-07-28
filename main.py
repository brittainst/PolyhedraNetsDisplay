# when program runs, it will prompt user to enter type of polyhedra net to open, and the
# number of that net (according to the database) to open. it will then draw the net

from functions import *

# creates name of the file that needs to be open
name = input("Enter the type of polyhedra:")
number = input("Enter the net number:")
filename = name + str(number) + 'Net' + '.json'

data = loadfile(name, number)
v = np.array(data.get("Vertices"))  # Calls database entry as a list and then converts to an array
e = np.array(data.get("Edges"))  # Calls database entry as a list and then converts to an array
x = data.keys()  # Stores as a list the names of all the entries in the dictionary.
f = np.array(data.get("Faces"))
facegraph = np.array(data["FaceGraph"]["AdjMat"].get("matrix"))

print('Radius of Gyration = ' + str(radiusg(v, f)))
graphnet(v, e, 'blue')  # Plots the net
print('Number of Vertex Connections = ' + str(countvc(name, v, e)))
graphnet(findcenters(v, f), facegraph, 'red')  # plots spanning tree of the net
# print(facegraph)
# print(f)
plt.axis('scaled')  # Preserves 1:1 aspect ratio
plt.show()  # Plots the scatterplot
