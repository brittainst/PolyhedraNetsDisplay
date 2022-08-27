import json  # Allows us to read json files
# This file is just a product of something I was working on with Dr. Jungck.
# It just scans through the roughness of each net, to find the minimum and maximum roughness
# Also pulls out all possible values of roughness
from functions import *

name = "Icosahedron"

minrough = 1000
maxrough = 0
possible_values = []
for i in range(43380):
    # calls the appropriate file from the database and stores it as the dictionary data
    filename = name + 'Net' + str(i).zfill(5) + '.json'
    data = loadfile(filename)
    roughness = data["NetInfo"].get("Roughness")
    if roughness > maxrough:
        maxrough = roughness
    if roughness < minrough:
        minrough = roughness
    if roughness not in possible_values:
        possible_values.append(roughness)
print("maximum roughness = " + str(maxrough))
print("minimum roughness = " + str(minrough))
print("possible values" + str(possible_values))
print(len(possible_values))
