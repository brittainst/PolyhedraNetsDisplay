from functions import *


# gets user input on which file to open
# name = input("Enter the type of polyhedra:")
# number = input("Enter the net number:")


def origami_creator(net_name=' ', net_number=-1, location=' ', plot=False):
    if net_name == ' ':
        net_name = input("Enter the type of polyhedra:")
    if net_number == -1:
        net_number = input("Enter the net number:")
    plot1 = plt.figure(1)
    data = loadFile(net_name, net_number)  # Stores net information as a dictionary
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

    # Determines the correct fold_angle for the origami based on the type of net
    fold_angle = 1
    if net_name == 'Tetrahedron':
        fold_angle = np.arccos(1/3)
    elif net_name == 'Cube':
        fold_angle = math.pi/2
    elif net_name == 'Octahedron':
        fold_angle = np.arccos(-1/3)
    elif net_name == 'Dodecahedron':
        fold_angle = np.arccos(-np.sqrt(5)/5)
    elif net_name == 'Icosahedron':
        fold_angle = np.arccos(-np.sqrt(5)/3)

    graphNet(v, interior_edges, 'b', 1-fold_angle/math.pi, False, '-')
    graphNet(v, edges, 'k', 1, False, '-')
    plt.axis('scaled')  # Preserves 1:1 aspect ratio
    plt.axis('off')
    if location == ' ':
        plt.savefig(str(net_name + net_number) + '.svg', format='svg', dpi=900)
    else:
        plt.savefig(location, dpi=900)

    if plot:
        plt.show()

# origami_creator(location=' ', plot=True)
