from functions import *
from origami import origami_creator
from PIL import ImageTk
from tkinter import filedialog
import os

# Creates the Main window of the GUI
master_window = tk.Tk()
master_window.geometry("1200x600")
master_window.title("Polyhedra Nets Display")

# Create First Frame
frame1 = tk.Frame(master_window)
frame1.pack(fill=tk.Y, side=tk.LEFT)
frame2 = tk.Frame(master_window)
frame2.pack(fill=tk.Y, side=tk.LEFT)
frame3 = tk.Frame(master_window)
frame3.pack(fill=tk.Y, side=tk.LEFT)

# Net Type Selection
name_label = tk.Label(master=frame1, text="Net Type")
name_label.pack()
name_entry = StringVar(master_window)
name_entry.set("Dodecahedron")

# Net Number Selection
number_label = tk.Label(master=frame1, text="Net Number")
# number_descriptor = tk.Label(text="Enter a number between 0 and " + str(num_of_nets(name_entry.get())-1))
num = StringVar()
number_entry = tk.Entry(frame1, textvariable=num, width=5)

# def update_num_of_nets():
#     new_number = num_of_nets(name_entry.get())-1
#     number_descriptor.config(text="Enter a number between 0 and " + str(new_number))
#     print(3)


w = OptionMenu(frame1, name_entry, "Tetrahedron", "Cube", "Octahedron", "Dodecahedron", "Icosahedron")
w.pack()

number_label.pack()
# number_descriptor.pack()
number_entry.pack()

def return_function():
    plt.close()
    name = name_entry.get()
    number = str(number_entry.get()).zfill(concat_length(name))
    drawNet(name, str(number), numberfaces=num_face.get(), vc=plot_vc.get(), showVertices=show_vertices.get(),
            spanning=show_spanning.get())
    if show_convex_hull.get() and name_entry.get() == "Dodecahedron":
        [convex_area, convex_perimeter] = convex_hull(name, number, True)
    plt.axis('off')
    plt.savefig("temporary", dpi=100)
    img = ImageTk.PhotoImage(file="temporary.png")
    label1.image = img
    label1.pack()
    label1.config(image=img)
    leaf_label.pack()
    num_of_leaves = leaves(name, number)
    leaf_label.config(text="Leaves: " + str(len(num_of_leaves)))

    data = loadFile(name, number)
    v = np.array(data.get("Vertices"))
    e = np.array(data.get("Edges"))
    f = np.array(data.get("Faces"))
    cmp_string = np.array(data.get("CmpString"))
    hamiltonian_entry.delete(0, END)
    hamiltonian_entry.insert(0, cmp_string)

    num_vc = countVC(name, v, e, False)
    vc_label.pack()
    vc_label.config(text="Vertex Connections: " + str(num_vc))

    rg_label.pack()
    net_rg = radius_of_gyration(v, f)
    rg_label.config(text="Radius of Gyration: " + str(net_rg))

    # diameter_label.pack()
    # diam = diameter(name, number)
    # diameter_label.config(text="Diameter: " + str(diam))

    if show_convex_hull.get() and name_entry.get() == "Dodecahedron":
        convex_area_label.config(text="Area of Convex Hull: " + str(convex_area))
        convex_area_label.pack()
        convex_perim_label.config(text="Perimeter of Covnex Hull: " + str(convex_perimeter))
        convex_perim_label.pack()


B = Button(frame1, text="Generate Net", command=return_function)
B.pack()

hamiltonian_label = tk.Label(master=frame1, text="Search by Hamiltonian Cycle")
hamiltonian_label.pack()

hamiltonian_entry = tk.Entry(frame1)
hamiltonian_entry.pack()

def search_by_hamiltonian():
    hamil = hamiltonian_entry.get()
    name_entry.set(net_type_from_string_length(hamil))
    number_entry.delete(0, END)
    number_entry.insert(0, str(find_net_number(hamil)))
    return_function()


search_button = Button(frame1, text="search", command=search_by_hamiltonian)
search_button.pack()

label1 = Label(frame2)
leaf_label = Label(frame3, width=50, anchor='w')
vc_label = Label(frame3, width=50, anchor='w')
rg_label = Label(frame3, width=50, anchor='w')
convex_area_label = Label(frame3, width=50, anchor='w')
convex_perim_label = Label(frame3, width=50, anchor='w')
diameter_label = Label(frame3, width=50, anchor='w')




num_face = tk.BooleanVar()
show_vertices = tk.BooleanVar()
plot_vc = tk.BooleanVar()
show_spanning = tk.BooleanVar()
show_convex_hull = tk.BooleanVar()

c1 = tk.Checkbutton(frame1, text='number faces', variable=num_face, onvalue=True, offvalue=False,
                    command=return_function, width=20, anchor='w')
c1.pack()
c2 = tk.Checkbutton(frame1, text='show vertices', variable=show_vertices, onvalue=True, offvalue=False,
                    command=return_function, width=20, anchor='w')
c2.pack()
c3 = tk.Checkbutton(frame1, text='show vertex connections', variable=plot_vc, onvalue=True, offvalue=False,
                    command=return_function, width=20, anchor='w')
c3.pack()
c4 = tk.Checkbutton(frame1, text='show spanning tree', variable=show_spanning, onvalue=True, offvalue=False,
                    command=return_function, width=20, anchor='w')
c4.pack()
c5 = tk.Checkbutton(frame1, text='Convex Hull', variable=show_convex_hull, onvalue=True, offvalue=False,
                    command=return_function, width=20, anchor='w')
c5.pack()

def save():
    my_filetypes = [('SVG', '.svg')]
    location_and_name = filedialog.asksaveasfilename(parent=master_window,
                                                     initialdir=os.getcwd(),
                                                     title="Please select a file name for saving:",
                                                     filetypes=my_filetypes)
    name = name_entry.get()
    number = str(number_entry.get()).zfill(concat_length(name))
    origami_creator(net_name=name, net_number=number, location=location_and_name, plot=False)


B2 = Button(frame1, text="Save Origami as SVG", command=save)
B2.pack()

# The following lines make sure the python script actually closes when the window is closed
def close():
    master_window.quit()
    master_window.destroy()


master_window.protocol("WM_DELETE_WINDOW", close)

master_window.mainloop()
