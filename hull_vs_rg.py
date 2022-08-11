# This file generates area of convex hull and radius of gyration data for every Dodecahedron Dürer net
# It then plots them both on a scatter plot.
# The file test.py has the arrays produced from ch_list and rg_list in this file directly in the code.
from functions import *

# Sets the net type to "Dodecahedron" because the convex hull script only works for those nets for now
name = "Dodecahedron"

# Initiates two lists/arrays to store the data on convex hulls and radius of gyration
ch_list = []
rg_list = []

# This for loop finds the area of the convex hull and the radius of gyration for each net, and then appends them to
# ch_list and rg_list respectively
for number in range(43380):
    # Calls the appropriate file in the database
    filename = name + 'Net' + str(number).zfill(5) + '.json'
    data = loadfile(filename)

    # Stores the vertices and faces of the Dürer net as the arrays v and f
    v = np.array(data.get("Vertices"))
    f = np.array(data.get("Faces"))

    # Calculates hull_area by calling the function convex_hull which returns the area of the convex hull
    # The last boolean input tells the function whether or not to attempt to plot the convex hull on a diagram,
    # so it's therefore set to FALSE so that it just returns the area and doesn't try to plot anything.
    hull_area = convex_hull(name, str(number).zfill(5), False)[0]

    # Calculates the radius of gyration by calling the radiusg function
    rg = radiusg(v, f)

    # Appends the data found for this net to the appropriate lists
    ch_list.append(hull_area)
    rg_list.append(rg)

# plots the radius of gyration versus the convex hull by making a scatter plot of the two arrays we created
plt.scatter(ch_list, rg_list, s=20, alpha=0.1, edgecolors="k")

# Names the x-axis and y-axis, and gives the graph a title
plt.xlabel("Area of Convex Hull")
plt.ylabel("Radius of Gyration")
plt.title("Radius of Gyration versus Area of Convex Hull of Dodecahedron Nets")

# This formula finds the slope and y-intercept of the line of best fit for the data
b, a = np.polyfit(ch_list, rg_list, deg=1)

# Creates an evenly spaced list of xvalue that will be used to plot the line of best fit
xseq = np.linspace(25, 45, num=200)

# Plots the line of best fit of the data
plt.plot(xseq, a + b * xseq, color="k", lw=2.5)

# Calculates the correlation and R^2 value for the data
correlation = np.corrcoef(ch_list, rg_list)[0, 1]
r_squared = correlation ** 2

print("R^2 is " + str(r_squared))  # Outputs what the value of R^2 is
plt.savefig("rg_versus_ch graph", dpi=900)  # Saves the output file
plt.show()  # Makes the plot visible
