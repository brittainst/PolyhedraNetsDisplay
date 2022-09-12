import json  # Allows us to read json files
# It just scans through the roughness of each net, to find the minimum and maximum roughness
# Also pulls out all possible values of roughness
from functions import *

name = "Icosahedron"

minRough = 1000
maxRough = 0
possible_values = []
for i in range(43380):
    # calls the appropriate file from the database and stores it as the dictionary data
    #TODO: loadfile thing
    data = loadFile(name, str(i).zfill(5))
    roughness = data["NetInfo"].get("Roughness")
    if roughness > maxRough:
        maxRough = roughness
    if roughness < minRough:
        minRough = roughness
    if roughness not in possible_values:
        possible_values.append(roughness)
print("maximum roughness = " + str(maxRough))
print("minimum roughness = " + str(minRough))
print("possible values" + str(possible_values))
print(len(possible_values))
