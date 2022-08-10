from functions import *

array = [35048, 43253, 43374, 19031, 27884, 22840, 41635, 16750, 10337, 33987, 9025, 23207, 33980, 40881, 32036, 5886,
         8905, 30578, 35386, 26228, 24269, 10228, 20504, 13528, 42771, 14505, 526]

for i in array:
    filename = "Dodecahedron" + 'Net' + str(i).zfill(5) + '.json'

    data = loadfile(filename)
    v = np.array(data.get("Vertices"))  # Calls database entry as a list and then converts to an array
    e = np.array(data.get("Edges"))  # Calls database entry as a list and then converts to an array
    x = data.keys()  # Stores as a list the names of all the entries in the dictionary.
    f = np.array(data.get("Faces"))
    rg = round(radiusg(v, f), 5)
    ch = round(convex_hull("Dodecahedron", str(i).zfill(5), False), 5)
    print("NETID:" + str(i).zfill(5) + "  Radius of Gyration: " + str(rg) + "  Area of Convex Hull: " + str(ch))