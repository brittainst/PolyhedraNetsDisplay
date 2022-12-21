from functions import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import ImageTk, Image


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
number_entry = tk.Entry(frame1)

# def update_num_of_nets():
#     new_number = num_of_nets(name_entry.get())-1
#     number_descriptor.config(text="Enter a number between 0 and " + str(new_number))
#     print(3)


w = OptionMenu(frame1, name_entry, "Tetrahedron", "Cube", "Octahedron", "Dodecahedron", "Icosahedron")
w.pack()

number_label.pack()
# number_descriptor.pack()
number_entry.pack()

label1 = Label(frame2)
leaf_label = Label(frame3)
vc_label = Label(frame3)
rg_label = Label(frame3)

def return_function():
    plt.close()
    name = name_entry.get()
    number = str(number_entry.get()).zfill(concat_length(name))
    drawNet(name, str(number), numberfaces=num_face.get(), vc=plot_vc.get(), showVertices=show_vertices.get(),
            spanning=show_spanning.get())
    plt.axis('off')
    plt.savefig("temporary", dpi=100)
    img = ImageTk.PhotoImage(file="temporary.png")
    label1.image = img
    label1.pack()
    label1.config(image=img)
    leaf_label.pack()
    num_of_leaves = leaves(name, number)
    leaf_label.config(text = "Leaves: " + str(len(num_of_leaves)))

    data = loadFile(name, number)
    v = np.array(data.get("Vertices"))
    e = np.array(data.get("Edges"))
    f = np.array(data.get("Faces"))
    num_vc = countVC(name, v, e, False)
    vc_label.pack()
    vc_label.config(text="Vertex Connections: " + str(num_vc))
    rg_label.pack()
    net_rg = radius_of_gyration(v,f)
    rg_label.config(text="Radius of Gyration: " + str(net_rg))


num_face = tk.BooleanVar()
show_vertices = tk.BooleanVar()
plot_vc = tk.BooleanVar()
show_spanning = tk.BooleanVar()
c1 = tk.Checkbutton(frame1, text='number faces', variable=num_face, onvalue=True, offvalue=False,
                    command=return_function, anchor='w')
c1.pack()
c2 = tk.Checkbutton(frame1, text='show vertices', variable=show_vertices, onvalue=True, offvalue=False,
                    command=return_function, anchor='w')
c2.pack()
c3 = tk.Checkbutton(frame1, text='show vertex connections', variable=plot_vc, onvalue=True, offvalue=False,
                    command=return_function, anchor='w')
c3.pack()
c4 = tk.Checkbutton(frame1, text='show spanning tree', variable=show_spanning, onvalue=True, offvalue=False,
                    command=return_function, anchor='w')
c4.pack()

B = Button(frame1, text="Generate Net", command=return_function)
B.pack()
master_window.mainloop()
