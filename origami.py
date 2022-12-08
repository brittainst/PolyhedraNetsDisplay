from functions import *

# gets user input on which file to open
name = input("Enter the type of polyhedra:")
number = input("Enter the net number:")

plot1 = plt.figure(1)
data = loadFile(name, number)  # Stores net information as a dictionary
v = np.array(data.get("Vertices"))  # stores vertices of Dürer net
durer_edges = np.array(data.get("Edges"))  # stores edges of Dürer net
f = np.array(data.get("Faces"))  # stores faces of Dürer net

# edges is a new array to hold the edges that make up the outer boundary of the Dürer net
edges = []
interior_edges = []

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
    else:
        interior_edges.append(durer_edges[i])
graphNet(v, interior_edges, 'b', 0.23227777777, False, '-')
graphNet(v, edges, 'k', 1, False, '-')
plt.axis('scaled')  # Preserves 1:1 aspect ratio
plt.axis('off')
plt.savefig(str(name+number)+'.svg', format='svg', dpi=900)
plt.show()
