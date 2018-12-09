from Functions import *
from PIL import Image as PILImage
from PIL import ImageTk
from random import randint
from sys import argv
from tkinter import *


class PaletteImage:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.palette = {
            "tree": FunctionNode(0.8),
            "values": [],
            "breakpoints": {},
            "domain": []
        }
        self.generate()
        self.generate_breakpoints()

    def generate(self):
        values = []
        for y in range(self.height):
            adjusted_y = 2 * y / self.height
            for x in range(self.width):
                adjusted_x = 2 * x / self.width
                values.append(self.palette["tree"].eval(adjusted_x, adjusted_y))
        self.palette["values"] = values
        self.palette["domain"] = [min(values), max(values)]

    def generate_breakpoints(self):
        sorted_values = self.palette["values"].copy()
        sorted_values.sort()

        for i in range(0, 101):
            self.palette["breakpoints"][i] = sorted_values[int((len(sorted_values) - 1) * i / 100)]

    def new(self, complexity=0.8):
        self.palette["tree"] = FunctionNode(complexity)
        self.generate()
        self.generate_breakpoints()


class GUI:
    class Preview:
        def __init__(self, master):
            self.master = master
            self.frame = Frame(self.master)
            self.palette_image = PaletteImage(600, 400)
            self.pil_image = PILImage.new("RGB", (600, 400))
            self.tk_image = ImageTk.PhotoImage(image=self.pil_image)
            self.label = Label(self.master, image=self.tk_image)
            self.label.pack()
            self.colors = [(0, 0, 0), (64, 64, 64), (128, 128, 128), (192, 192, 192), (255, 255, 255)]
            self.data = []
            self.breakpoints = []

        def update_breakpoints(self):
            data = []
            for v in self.palette_image.palette["values"]:
                if v < self.palette_image.palette["breakpoints"][self.breakpoints[0]]:
                    data.append(0)
                elif v < self.palette_image.palette["breakpoints"][self.breakpoints[1]]:
                    data.append(1)
                elif v < self.palette_image.palette["breakpoints"][self.breakpoints[2]]:
                    data.append(2)
                elif v < self.palette_image.palette["breakpoints"][self.breakpoints[3]]:
                    data.append(3)
                else:
                    data.append(4)
            self.data = data

        def update_image(self):
            self.update_breakpoints()
            data = [self.colors[i] for i in self.data]
            self.pil_image.putdata(data)
            self.tk_image = ImageTk.PhotoImage(image=self.pil_image)
            self.label.destroy()
            self.label = Label(self.master, image=self.tk_image)
            self.label.pack()

    def __init__(self, master):
        self.master = master
        self.frame = Frame(self.master)
        self.preview = self.Preview(Toplevel(self.master))

        Label(self.master, text="Colors").grid(row=0, column=0)
        Label(self.master, text="R").grid(row=0, column=1)
        Label(self.master, text="G").grid(row=0, column=2)
        Label(self.master, text="B").grid(row=0, column=3)
        Label(self.master, text="Range").grid(row=0, column=4, columnspan=2)

        self.colors = [
            {
                "r": IntVar(master=self.master, value=randint(0, 255)),
                "r_entry": Entry(self.master),
                "g": IntVar(master=self.master, value=randint(0, 255)),
                "g_entry": Entry(self.master),
                "b": IntVar(master=self.master, value=randint(0, 255)),
                "b_entry": Entry(self.master),
                "range": Scale(master=self.master, from_=0, to_=100, orient=HORIZONTAL, command=self.update_color),
                "swatch": Canvas(self.master, width=32, height=32)
            },
            {
                "r": IntVar(master=self.master, value=randint(0, 255)),
                "r_entry": Entry(self.master),
                "g": IntVar(master=self.master, value=randint(0, 255)),
                "g_entry": Entry(self.master),
                "b": IntVar(master=self.master, value=randint(0, 255)),
                "b_entry": Entry(self.master),
                "range": Scale(master=self.master, from_=0, to_=100, orient=HORIZONTAL, command=self.update_color),
                "swatch": Canvas(self.master, width=32, height=32)
            },
            {
                "r": IntVar(master=self.master, value=randint(0, 255)),
                "r_entry": Entry(self.master),
                "g": IntVar(master=self.master, value=randint(0, 255)),
                "g_entry": Entry(self.master),
                "b": IntVar(master=self.master, value=randint(0, 255)),
                "b_entry": Entry(self.master),
                "range": Scale(master=self.master, from_=0, to_=100, orient=HORIZONTAL, command=self.update_color),
                "swatch": Canvas(self.master, width=32, height=32)
            },
            {
                "r": IntVar(master=self.master, value=randint(0, 255)),
                "r_entry": Entry(self.master),
                "g": IntVar(master=self.master, value=randint(0, 255)),
                "g_entry": Entry(self.master),
                "b": IntVar(master=self.master, value=randint(0, 255)),
                "b_entry": Entry(self.master),
                "range": Scale(master=self.master, from_=0, to_=100, orient=HORIZONTAL, command=self.update_color),
                "swatch": Canvas(self.master, width=32, height=32)
            },
            {
                "r": IntVar(master=self.master, value=randint(0, 255)),
                "r_entry": Entry(self.master),
                "g": IntVar(master=self.master, value=randint(0, 255)),
                "g_entry": Entry(self.master),
                "b": IntVar(master=self.master, value=randint(0, 255)),
                "b_entry": Entry(self.master),
                "swatch": Canvas(self.master, width=32, height=32)
            }
        ]

        i = 1
        for c in self.colors:
            c["swatch"].grid(row=i, column=0)
            c["r_entry"].configure(textvariable=c["r"])
            c["g_entry"].configure(textvariable=c["g"])
            c["b_entry"].configure(textvariable=c["b"])
            c["r"].trace_add("write", self.update_color)
            c["g"].trace_add("write", self.update_color)
            c["b"].trace_add("write", self.update_color)
            c["r_entry"].grid(row=i, column=1)
            c["g_entry"].grid(row=i, column=2)
            c["b_entry"].grid(row=i, column=3)
            if i != 5:
                c["range"].grid(row=i, column=4, columnspan=2)
                c["range"].set(randint((i - 1) * 20, i * 20))
            i += 1

        self.new_button = Button(self.master, text="New Tree", command=self.new)
        self.new_button.grid(row=6, column=0)
        self.save_name = Entry(self.master)
        self.save_name.grid(row=6, column=1, columnspan=4)
        self.save_name.insert(0, "test")
        self.save_button = Button(self.master, text="Save", command=self.save)
        self.save_button.grid(row=6, column=5)

    def update_color(self, n1=None, n2=None, n3=None):
        self.colors[0]["range"].configure(from_=0, to_=self.colors[1]["range"].get())
        self.colors[1]["range"].configure(from_=self.colors[0]["range"].get(), to_=self.colors[2]["range"].get())
        self.colors[2]["range"].configure(from_=self.colors[1]["range"].get(), to_=self.colors[3]["range"].get())
        self.colors[3]["range"].configure(from_=self.colors[2]["range"].get(), to_=100)

        for i in range(len(self.colors)):
            try:
                c = (int(self.colors[i]["r"].get()), int(self.colors[i]["g"].get()), int(self.colors[i]["b"].get()))
                self.preview.colors[i] = c
                self.colors[i]["swatch"].configure(bg="#%02x%02x%02x" % c)
            except TclError:
                pass

        self.preview.breakpoints = [self.colors[i]["range"].get() for i in range(4)]
        self.preview.update_image()

    def new(self):
        self.preview.palette_image.new()
        self.preview.update_breakpoints()
        self.preview.update_image()

    def save(self):
        palette_image = PaletteImage(1200, 800)
        palette_image.palette["tree"] = self.preview.palette_image.palette["tree"]
        palette_image.generate()
        palette_image.generate_breakpoints()
        data = []
        for v in palette_image.palette["values"]:
            if v < palette_image.palette["breakpoints"][self.preview.breakpoints[0]]:
                data.append(0)
            elif v < palette_image.palette["breakpoints"][self.preview.breakpoints[1]]:
                data.append(1)
            elif v < palette_image.palette["breakpoints"][self.preview.breakpoints[2]]:
                data.append(2)
            elif v < palette_image.palette["breakpoints"][self.preview.breakpoints[3]]:
                data.append(3)
            else:
                data.append(4)
        new_data = [self.preview.colors[i] for i in data]
        final_image = PILImage.new("RGB", (1200, 800))
        final_image.putdata(new_data)
        final_image.save(self.save_name.get() + ".png", "PNG")


def save_palette(width, height, name, fuzzy):
    palette_image = PaletteImage(width, height)
    breakpoints = [20, 40, 60, 80]
    data = []
    if fuzzy:
        for v in palette_image.palette["values"]:
            if v < palette_image.palette["breakpoints"][breakpoints[0] + randint(-5, 5)]:
                data.append(0)
            elif v < palette_image.palette["breakpoints"][breakpoints[1] + randint(-5, 5)]:
                data.append(1)
            elif v < palette_image.palette["breakpoints"][breakpoints[2] + randint(-5, 5)]:
                data.append(2)
            elif v < palette_image.palette["breakpoints"][breakpoints[3] + randint(-5, 5)]:
                data.append(3)
            else:
                data.append(4)
    else:
        for v in palette_image.palette["values"]:
            if v < palette_image.palette["breakpoints"][breakpoints[0]]:
                data.append(0)
            elif v < palette_image.palette["breakpoints"][breakpoints[1]]:
                data.append(1)
            elif v < palette_image.palette["breakpoints"][breakpoints[2]]:
                data.append(2)
            elif v < palette_image.palette["breakpoints"][breakpoints[3]]:
                data.append(3)
            else:
                data.append(4)
    colors = [(randint(0, 255), randint(0, 255), randint(0, 255)),
              (randint(0, 255), randint(0, 255), randint(0, 255)),
              (randint(0, 255), randint(0, 255), randint(0, 255)),
              (randint(0, 255), randint(0, 255), randint(0, 255)),
              (randint(0, 255), randint(0, 255), randint(0, 255))]
    new_data = [colors[i] for i in data]
    final_image = PILImage.new("RGB", (width, height))
    final_image.putdata(new_data)
    final_image.save(name + ".png", "PNG")


if __name__ == "__main__":
    if "-gui" in argv:
        root = Tk()
        gui = GUI(root)
        root.mainloop()
    else:
        width = 1200
        height = 800
        name = "test"
        fuzzy = "-fuzzy" in argv
        if "-width" in argv:
            width = int(argv[argv.index("-width") + 1])
        if "-height" in argv:
            height = int(argv[argv.index("-height") + 1])
        if "-name" in argv:
            name = argv[argv.index("-name") + 1]
        save_palette(width, height, name, fuzzy)
