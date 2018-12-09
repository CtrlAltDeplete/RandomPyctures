import multiprocessing

from Functions import *
from PIL import Image as PILImage
from PIL import ImageTk
from random import randint
from sys import argv
from tkinter import *


class RGBImage:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.red = {
            "tree": FunctionNode(0.6),
            "values": [],
            "shift": randint(0, 255),
            "range": randint(1, 256)
        }
        self.green = {
            "tree": FunctionNode(0.6),
            "values": [],
            "shift": randint(0, 255),
            "range": randint(1, 256)
        }
        self.blue = {
            "tree": FunctionNode(0.6),
            "values": [],
            "shift": randint(0, 255),
            "range": randint(1, 256)
        }
        self.generate()

    def generate(self):
        manager = multiprocessing.Manager()
        return_dict = manager.dict()

        jobs = []
        for func in self._generate_reds, self._generate_greens, self._generate_blues:
            p = multiprocessing.Process(target=func, args=(return_dict,))
            jobs.append(p)
            p.start()
        for proc in jobs:
            proc.join()

        self.red["values"] = return_dict["red"]
        self.green["values"] = return_dict["green"]
        self.blue["values"] = return_dict["blue"]

    def _generate_reds(self, return_dict=None):
        values = []
        for y in range(self.height):
            adjusted_y = 2 * y / self.height
            for x in range(self.width):
                adjusted_x = 2 * x / self.width
                values.append(self.red["tree"].eval(adjusted_x, adjusted_y))
        if return_dict is not None:
            return_dict["red"] = values
        else:
            self.red["values"] = values

    def _generate_greens(self, return_dict=None):
        values = []
        for y in range(self.height):
            adjusted_y = 2 * y / self.height
            for x in range(self.width):
                adjusted_x = 2 * x / self.width
                values.append(self.green["tree"].eval(adjusted_x, adjusted_y))
        if return_dict is not None:
            return_dict["green"] = values
        else:
            self.green["values"] = values

    def _generate_blues(self, return_dict=None):
        values = []
        for y in range(self.height):
            adjusted_y = 2 * y / self.height
            for x in range(self.width):
                adjusted_x = 2 * x / self.width
                values.append(self.blue["tree"].eval(adjusted_x, adjusted_y))
        if return_dict is not None:
            return_dict["blue"] = values
        else:
            self.blue["values"] = values

    def _new_red(self, complexity=0.6):
        self.red["tree"] = FunctionNode(complexity)
        self._generate_reds()

    def _new_green(self, complexity=0.6):
        self.green["tree"] = FunctionNode(complexity)
        self._generate_greens()

    def _new_blue(self, complexity=0.6):
        self.blue["tree"] = FunctionNode(complexity)
        self._generate_blues()

    def new(self, complexity=(0.6, 0.6, 0.6)):
        self.red["tree"] = FunctionNode(complexity[0])
        self.green["tree"] = FunctionNode(complexity[1])
        self.blue["tree"] = FunctionNode(complexity[2])
        self.generate()


class GUI:
    class Preview:
        def __init__(self, master):
            self.master = master
            self.frame = Frame(self.master)
            self.rgb_image = RGBImage(600, 400)
            self.pil_image = PILImage.new("RGB", (600, 400))
            self.tk_image = ImageTk.PhotoImage(image=self.pil_image)
            self.label = Label(self.master, image=self.tk_image)
            self.label.pack()
            self.visibilities = [True, True, True]
            self.bands = [PILImage.new("L", (600, 400)), PILImage.new("L", (600, 400)), PILImage.new("L", (600, 400))]

        def _generate_red_band(self, return_dict=None):
            data = []
            for i in self.rgb_image.red["values"]:
                data.append(((i / 2 + 0.5) * self.rgb_image.red["range"] + self.rgb_image.red["shift"]) % 256)
            if return_dict:
                img = PILImage.new("L", (600, 400))
                img.putdata(data)
                return_dict["red_band"] = img
            else:
                self.bands[0].putdata(data)

        def _generate_green_band(self, return_dict=None):
            data = []
            for i in self.rgb_image.green["values"]:
                data.append(((i / 2 + 0.5) * self.rgb_image.green["range"] + self.rgb_image.green["shift"]) % 256)
            if return_dict:
                img = PILImage.new("L", (600, 400))
                img.putdata(data)
                return_dict["green_band"] = img
            else:
                self.bands[1].putdata(data)

        def _generate_blue_band(self, return_dict=None):
            data = []
            for i in self.rgb_image.blue["values"]:
                data.append(((i / 2 + 0.5) * self.rgb_image.blue["range"] + self.rgb_image.blue["shift"]) % 256)
            if return_dict:
                img = PILImage.new("L", (600, 400))
                img.putdata(data)
                return_dict["blue_band"] = img
            else:
                self.bands[2].putdata(data)

        def generate(self):
            manager = multiprocessing.Manager()
            return_dict = manager.dict()

            jobs = []
            for func in self._generate_red_band, self._generate_green_band, self._generate_blue_band:
                p = multiprocessing.Process(target=func, args=(return_dict,))
                jobs.append(p)
                p.start()
            for proc in jobs:
                proc.join()

            self.bands = return_dict["red_band"], return_dict["green_band"], return_dict["blue_band"]

        def update(self):
            bands = []
            if self.visibilities[0]:
                bands.append(self.bands[0])
            else:
                bands.append(PILImage.new("L", (600, 400), color=self.rgb_image.red["shift"]))
            if self.visibilities[1]:
                bands.append(self.bands[1])
            else:
                bands.append(PILImage.new("L", (600, 400), color=self.rgb_image.green["shift"]))
            if self.visibilities[2]:
                bands.append(self.bands[2])
            else:
                bands.append(PILImage.new("L", (600, 400), color=self.rgb_image.blue["shift"]))
            self.pil_image = PILImage.merge("RGB", bands)
            self.tk_image = ImageTk.PhotoImage(image=self.pil_image)
            self.label.destroy()
            self.label = Label(self.master, image=self.tk_image)
            self.label.pack()

    def __init__(self, master):
        self.master = master
        self.frame = Frame(self.master)
        self.preview = self.Preview(Toplevel(self.master))

        Label(self.master, text="Tree").grid(row=0, column=1)
        Label(self.master, text="Shift").grid(row=0, column=2)
        Label(self.master, text="Range").grid(row=0, column=4)
        Label(self.master, text="Toggle").grid(row=0, column=6)
        Label(self.master, text="Red").grid(row=1, column=0)
        Label(self.master, text="Green").grid(row=2, column=0)
        Label(self.master, text="Blue").grid(row=3, column=0)

        self.new_red_button = Button(master=self.master, text="New Red", command=self.new_red_tree)
        self.new_red_button.grid(row=1, column=1)
        self.new_green_button = Button(master=self.master, text="New Green", command=self.new_green_tree)
        self.new_green_button.grid(row=2, column=1)
        self.new_blue_button = Button(master=self.master, text="New Blue", command=self.new_blue_tree)
        self.new_blue_button.grid(row=3, column=1)

        self.red_shift = Scale(self.master, from_=0, to_=254, orient=HORIZONTAL, command=self.update_red)
        self.red_shift.grid(row=1, column=2, columnspan=2)
        self.red_shift.set(self.preview.rgb_image.red["shift"])
        self.green_shift = Scale(self.master, from_=0, to_=254, orient=HORIZONTAL, command=self.update_green)
        self.green_shift.grid(row=2, column=2, columnspan=2)
        self.green_shift.set(self.preview.rgb_image.green["shift"])
        self.blue_shift = Scale(self.master, from_=0, to_=254, orient=HORIZONTAL, command=self.update_blue)
        self.blue_shift.grid(row=3, column=2, columnspan=2)
        self.blue_shift.set(self.preview.rgb_image.blue["shift"])

        self.red_range = Scale(self.master, from_=1, to_=256, orient=HORIZONTAL, command=self.update_red)
        self.red_range.grid(row=1, column=4, columnspan=2)
        self.red_range.set(self.preview.rgb_image.red["range"])
        self.green_range = Scale(self.master, from_=1, to_=256, orient=HORIZONTAL, command=self.update_green)
        self.green_range.grid(row=2, column=4, columnspan=2)
        self.green_range.set(self.preview.rgb_image.green["range"])
        self.blue_range = Scale(self.master, from_=1, to_=256, orient=HORIZONTAL, command=self.update_blue)
        self.blue_range.grid(row=3, column=4, columnspan=2)
        self.blue_range.set(self.preview.rgb_image.blue["range"])

        self.red_visible = Button(master=self.master, text="Hide", command=self.toggle_red)
        self.red_visible.grid(row=1, column=6)
        self.green_visible = Button(master=self.master, text="Hide", command=self.toggle_green)
        self.green_visible.grid(row=2, column=6)
        self.blue_visible = Button(master=self.master, text="Hide", command=self.toggle_blue)
        self.blue_visible.grid(row=3, column=6)

        self.save_name = Entry(self.master)
        self.save_name.grid(row=4, column=0, columnspan=5)
        self.save_name.insert(0, "test")
        self.save_button = Button(master=self.master, text="Save", command=self.save)
        self.save_button.grid(row=4, column=6)

    def update_red(self, n=None):
        self.preview.rgb_image.red["range"] = self.red_range.get()
        self.preview.rgb_image.red["shift"] = self.red_shift.get()
        self.preview._generate_red_band()
        self.preview.update()

    def new_red_tree(self):
        self.preview.rgb_image._new_red()
        self.preview._generate_red_band()
        self.preview.update()

    def update_green(self, n=None):
        self.preview.rgb_image.green["range"] = self.green_range.get()
        self.preview.rgb_image.green["shift"] = self.green_shift.get()
        self.preview._generate_green_band()
        self.preview.update()

    def new_green_tree(self):
        self.preview.rgb_image._new_green()
        self.preview._generate_green_band()
        self.preview.update()

    def update_blue(self, n=None):
        self.preview.rgb_image.blue["range"] = self.blue_range.get()
        self.preview.rgb_image.blue["shift"] = self.blue_shift.get()
        self.preview._generate_blue_band()
        self.preview.update()

    def new_blue_tree(self):
        self.preview.rgb_image._new_blue()
        self.preview._generate_blue_band()
        self.preview.update()

    def toggle_red(self):
        self.preview.visibilities[0] = not self.preview.visibilities[0]
        text = "Hide" if self.preview.visibilities[0] else "Show"
        self.red_visible.destroy()
        self.red_visible = Button(self.master, text=text, command=self.toggle_red)
        self.red_visible.grid(row=1, column=6)
        self.preview.update()

    def toggle_green(self):
        self.preview.visibilities[1] = not self.preview.visibilities[1]
        text = "Hide" if self.preview.visibilities[1] else "Show"
        self.green_visible.destroy()
        self.green_visible = Button(self.master, text=text, command=self.toggle_green)
        self.green_visible.grid(row=2, column=6)
        self.preview.update()

    def toggle_blue(self):
        self.preview.visibilities[2] = not self.preview.visibilities[2]
        text = "Hide" if self.preview.visibilities[2] else "Show"
        self.blue_visible.destroy()
        self.blue_visible = Button(self.master, text=text, command=self.toggle_blue)
        self.blue_visible.grid(row=3, column=6)
        self.preview.update()

    def save(self):
        visibility = self.preview.visibilities
        color = self.preview.rgb_image.red, self.preview.rgb_image.green, self.preview.rgb_image.blue
        bands = [generate_band(1200, 800, visibility[i], color[i]["tree"], color[i]["shift"], color[i]["range"]) for i in range(3)]

        final_image = PILImage.merge("RGB", bands)
        final_image.save(self.save_name.get() + ".png", "PNG")


def generate_band(width, height, visible, head, shift, stretch):
    if visible:
        band = PILImage.new("L", (width, height))
        data = []
        for y in range(height):
            adjusted_y = 2 * y / height
            for x in range(width):
                adjusted_x = 2 * x / width
                data.append(((head.eval(adjusted_x, adjusted_y) / 2 + 0.5) * stretch + shift) % 256)
        band.putdata(data)
    else:
        band = PILImage.new("L", (width, height), color=shift)
    return band


def save_RGB(width, height, name):
    rgb_image = RGBImage(width, height)
    color = rgb_image.red, rgb_image.green, rgb_image.blue
    bands = [generate_band(width, height, True, color[i]["tree"], color[i]["shift"], color[i]["range"]) for i in range(3)]

    final_image = PILImage.merge("RGB", bands)
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
        if "-width" in argv:
            width = int(argv[argv.index("-width") + 1])
        if "-height" in argv:
            height = int(argv[argv.index("-height") + 1])
        if "-name" in argv:
            name = argv[argv.index("-name") + 1]
        save_RGB(width, height, name)
