from functions import *

name = "Dodecahedron"
ch_list = []
rg_list = []
# unique_ch_values = []
for number in range(43380):
    filename = name + 'Net' + str(number).zfill(5) + '.json'
    data = loadfile(filename)
    v = np.array(data.get("Vertices"))  # Calls database entry as a list and then converts to an array
    f = np.array(data.get("Faces"))
    hull_area = convex_hull(name, str(number).zfill(5), False)
    # if round(hull_area, 4) not in unique_ch_values:
    #    unique_ch_values.append(round(hull_area, 4))
    rg = radiusg(v, f)
    ch_list.append(hull_area)
    rg_list.append(rg)

# print(unique_ch_values)
# print(len(unique_ch_values))
plt.scatter(ch_list, rg_list, s=20, alpha=0.1, edgecolors="k")
plt.xlabel("Area of Convex Hull")
plt.ylabel("Radius of Gyration")
plt.title("Radius of Gyration versus Area of Convex Hull of Dodecahedron Nets")
b, a = np.polyfit(ch_list, rg_list, deg=1)
xseq = np.linspace(25, 45, num=200)
plt.plot(xseq, a + b * xseq, color="k", lw=2.5)
correlation = np.corrcoef(ch_list, rg_list)[0, 1]
r_squared = correlation ** 2
print("R^2 is " + str(r_squared))
plt.savefig("rg_versus_ch graph", dpi=900)
plt.show()
