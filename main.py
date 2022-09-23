# when program runs, it will prompt user to enter type of polyhedra net to open, and the
# number of that net (according to the database) to open. it will then draw the net
#TODO: time permitting, go through git history and pull back every variation we've done in main
# (just nets, convex hull, numbering faces, etc) to show how we've used our functions

from functions import *

# gets user input on which file to open
name = input("Enter the type of polyhedra:")
number = input("Enter the net number:")

# TODO: move these arrays to another file; used for related research but not to run main
'''
# an array of Dodecahedron net numbers, with three nets chosen from each class of vertex score
array = [35048, 43253, 43374, 19031, 27884, 22840, 41635, 16750, 10337, 33987, 9025, 23207, 33980, 40881, 32036, 5886,
         8905, 30578, 35386, 26228, 24269, 10228, 20504, 13528, 42771, 14505, 526]
# an array of all Dodecahedron net numbers that give a net with two vertex connections
array2 = [7725, 9023, 11463, 13645, 18975, 22159, 24417, 33681, 35048, 35934, 39346, 40685, 41417, 41971, 42758, 43227,
          43253, 43374]
'''

# starts a new matplotlib figure
# TODO: docstring for bounding circles, drawing nets
plot1 = plt.figure(1)
drawNet(name, str(number).zfill(5))
[area, perimeter] = convex_hull(name, str(number).zfill(5), True)
print(area)
print(perimeter)

# When uncommented, draws a bounding circle that is slightly too big
# radius = radius_bounding_circle(name, number, True)

# When uncommented, draws a bounding circle that is slightly too small
# radius2 = bounding_circle_2(name, number, True)
# print("Radius of bounding circle is " + str(radius) + ", " + str(radius2))

# UNCOMMENT FOR SCHLEGEL
# starts a new matplotlib figure
# plot2 = plt.figure(2)
# draws the corresponding Schlegel diagram
# draw_schlegel(name, number)

plt.show()
