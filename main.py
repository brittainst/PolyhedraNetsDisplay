# when program runs, it will prompt user to enter type of polyhedra net to open, and the
# number of that net (according to the database) to open. it will then draw the net

from functions import *

# creates name of the file that needs to be open
name = input("Enter the type of polyhedra:")


# number = input("Enter the net number:")

# todo: move drawnet to functions
def drawnet(name, number):
    filename = name + 'Net' + str(number) + '.json'

    data = loadfile(filename)
    v = np.array(data.get("Vertices"))  # Calls database entry as a list and then converts to an array
    e = np.array(data.get("Edges"))  # Calls database entry as a list and then converts to an array
    x = data.keys()  # Stores as a list the names of all the entries in the dictionary.
    f = np.array(data.get("Faces"))
    facegraph = np.array(data["FaceGraph"]["AdjMat"].get("matrix"))

    # print('Radius of Gyration = ' + str(radiusg(v, f)))
    graphnet(v, e, 'blue', False)  # Plots the net
    vertconnect = str(countvc(name, v, e, True))
    print('Number of Vertex Connections = ' + vertconnect)
    # print('The leaves are ' + str(leaves(name,number)))
    graphnet(findcenters(v, f), facegraph, 'red', False)  # plots spanning tree of the net
    # print(facegraph)
    firstface = f[0]
    xcoord = 0
    ycoord = 0
    for i in firstface:
        xcoord = xcoord + v[int(firstface[i])][0]
        ycoord = ycoord + v[int(firstface[i])][1]
    xcoord = xcoord / len(firstface)
    ycoord = ycoord / len(firstface)
    plt.text(xcoord, ycoord, str(number), fontsize=8, horizontalalignment='center',
             verticalalignment='center')
    plt.axis('scaled')  # Preserves 1:1 aspect ratio
    plt.xlabel(name + ' Net ' + number + ': V_c = ' + vertconnect)

    FaceCenters = findcenters(v, f)
    centermass = [0, 0]  # Initializes a variable for center of mass
    for center in FaceCenters:  # Averages the centers of the faces to find center of mass
        centermass = np.add(centermass, center)
    centermass[0] = centermass[0] / len(FaceCenters)
    centermass[1] = centermass[1] / len(FaceCenters)

    plt.xlim([centermass[0] - 7, centermass[0] + 7])
    plt.ylim([centermass[1] - 7, centermass[1] + 7])
    plt.savefig("output" + str(number) + ".jpg", dpi=600)
    plt.show()  # Plots the scatterplot


array = [35048, 43253, 43374, 19031, 27884, 22840, 41635, 16750, 10337, 33987, 9025, 23207, 33980, 40881, 32036, 5886,
         8905, 30578, 35386, 26228, 24269, 10228, 20504, 13528, 42771, 14505, 526]
array2 = [7725, 9023, 11463, 13645, 18975, 22159, 24417, 33681, 35048, 35934, 39346, 40685, 41417, 41971, 42758, 43227,
          43253, 43374]

for i in array2:
    number = str(i).zfill(5)
    drawnet(name, number)
