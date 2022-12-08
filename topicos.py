from functions import *
name = "Icosahedron"
for number in range(0, 43380):
    data = loadFile(name, str(number).zfill(5))
    v = np.array(data.get("Vertices"))
    e = np.array(data.get("Edges"))
    num = countVC(name, v, e, False)
    if num == 2:
        print(number)
