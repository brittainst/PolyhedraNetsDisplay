# when program runs, it will prompt user to enter type of polyhedra net to open, and the
# number of that net (according to the database) to open. it will then draw the net

from functions import *
#from make_dodecahedron_graph import *
# creates name of the file that needs to be open
name = input("Enter the type of polyhedra:")


number = input("Enter the net number:")



array = [35048, 43253, 43374, 19031, 27884, 22840, 41635, 16750, 10337, 33987, 9025, 23207, 33980, 40881, 32036, 5886,
         8905, 30578, 35386, 26228, 24269, 10228, 20504, 13528, 42771, 14505, 526]
array2 = [7725, 9023, 11463, 13645, 18975, 22159, 24417, 33681, 35048, 35934, 39346, 40685, 41417, 41971, 42758, 43227,
          43253, 43374]

#for i in array2:
#    number = str(i).zfill(5)
#    drawnet(name, number)
plot1 = plt.figure(1)
drawnet(name, number)
plot2 = plt.figure(2)
draw_schlegel(name, number)
plt.show()