import multiprocessing

from Functions import *
from PIL import Image as PILImage
from PIL import ImageTk
from random import randint
from sys import argv
from tkinter import *


class HSVImage:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.hue = {
            "tree": FunctionNode(0.6),
            "values": [],
            "shift": randint(0, 255),
            "range": randint(1, 256)
        }
        self.sat = {
            "tree": FunctionNode(0.6),
            "values": [],
            "shift": randint(0, 255),
            "range": randint(1, 256)
        }
        self.val = {
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
        for func in self._generate_hues, self._generate_sats, self._generate_vals:
            p = multiprocessing.Process(target=func, args=(return_dict,))
            jobs.append(p)
            p.start()
        for proc in jobs:
            proc.join()

        self.hue["values"] = return_dict["hue"]
        self.sat["values"] = return_dict["sat"]
        self.val["values"] = return_dict["val"]

    def _generate_hues(self, return_dict=None):
        values = []
        for y in range(self.height):
            adjusted_y = 2 * y / self.height
            for x in range(self.width):
                adjusted_x = 2 * x / self.width
                values.append(self.hue["tree"].eval(adjusted_x, adjusted_y))
        if return_dict is not None:
            return_dict["hue"] = values
        else:
            self.hue["values"] = values

    def _generate_sats(self, return_dict=None):
        values = []
        for y in range(self.height):
            adjusted_y = 2 * y / self.height
            for x in range(self.width):
                adjusted_x = 2 * x / self.width
                values.append(self.sat["tree"].eval(adjusted_x, adjusted_y))
        if return_dict is not None:
            return_dict["sat"] = values
        else:
            self.sat["values"] = values

    def _generate_vals(self, return_dict=None):
        values = []
        for y in range(self.height):
            adjusted_y = 2 * y / self.height
            for x in range(self.width):
                adjusted_x = 2 * x / self.width
                values.append(self.val["tree"].eval(adjusted_x, adjusted_y))
        if return_dict is not None:
            return_dict["val"] = values
        else:
            self.val["values"] = values

    def _new_hue(self, complexity=0.6):
        self.hue["tree"] = FunctionNode(complexity)
        self._generate_hues()

    def _new_sat(self, complexity=0.6):
        self.sat["tree"] = FunctionNode(complexity)
        self._generate_sats()

    def _new_val(self, complexity=0.6):
        self.val["tree"] = FunctionNode(complexity)
        self._generate_vals()

    def new(self, complexity=(0.6, 0.6, 0.6)):
        self.hue["tree"] = FunctionNode(complexity[0])
        self.sat["tree"] = FunctionNode(complexity[1])
        self.val["tree"] = FunctionNode(complexity[2])
        self.generate()


class GUI:
    class Preview:
        def __init__(self, master):
            self.master = master
            self.frame = Frame(self.master)
            self.hsv_image = HSVImage(600, 400)
            self.pil_image = PILImage.new("HSV", (600, 400))
            self.tk_image = ImageTk.PhotoImage(image=self.pil_image)
            self.label = Label(self.master, image=self.tk_image)
            self.label.pack()
            self.visibilities = [True, True, True]
            self.bands = [PILImage.new("L", (600, 400)), PILImage.new("L", (600, 400)), PILImage.new("L", (600, 400))]

        def _generate_hue_band(self, return_dict=None):
            data = []
            for i in self.hsv_image.hue["values"]:
                data.append(((i / 2 + 0.5) * self.hsv_image.hue["range"] + self.hsv_image.hue["shift"]) % 256)
            if return_dict:
                img = PILImage.new("L", (600, 400))
                img.putdata(data)
                return_dict["hue_band"] = img
            else:
                self.bands[0].putdata(data)

        def _generate_sat_band(self, return_dict=None):
            data = []
            for i in self.hsv_image.sat["values"]:
                data.append(((i / 2 + 0.5) * self.hsv_image.sat["range"] + self.hsv_image.sat["shift"]) % 256)
            if return_dict:
                img = PILImage.new("L", (600, 400))
                img.putdata(data)
                return_dict["sat_band"] = img
            else:
                self.bands[1].putdata(data)

        def _generate_val_band(self, return_dict=None):
            data = []
            for i in self.hsv_image.val["values"]:
                data.append(((i / 2 + 0.5) * self.hsv_image.val["range"] + self.hsv_image.val["shift"]) % 256)
            if return_dict:
                img = PILImage.new("L", (600, 400))
                img.putdata(data)
                return_dict["val_band"] = img
            else:
                self.bands[2].putdata(data)

        def generate(self):
            manager = multiprocessing.Manager()
            return_dict = manager.dict()

            jobs = []
            for func in self._generate_hue_band, self._generate_sat_band, self._generate_val_band:
                p = multiprocessing.Process(target=func, args=(return_dict,))
                jobs.append(p)
                p.start()
            for proc in jobs:
                proc.join()

            self.bands = return_dict["hue_band"], return_dict["sat_band"], return_dict["val_band"]

        def update(self):
            bands = []
            if self.visibilities[0]:
                bands.append(self.bands[0])
            else:
                bands.append(PILImage.new("L", (600, 400), color=self.hsv_image.hue["shift"]))
            if self.visibilities[1]:
                bands.append(self.bands[1])
            else:
                bands.append(PILImage.new("L", (600, 400), color=self.hsv_image.sat["shift"]))
            if self.visibilities[2]:
                bands.append(self.bands[2])
            else:
                bands.append(PILImage.new("L", (600, 400), color=self.hsv_image.val["shift"]))
            self.pil_image = PILImage.merge("HSV", bands)
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
        Label(self.master, text="Hue").grid(row=1, column=0)
        Label(self.master, text="Saturation").grid(row=2, column=0)
        Label(self.master, text="Value").grid(row=3, column=0)

        self.new_hue_button = Button(master=self.master, text="New Hue", command=self.new_hue_tree)
        self.new_hue_button.grid(row=1, column=1)
        self.new_sat_button = Button(master=self.master, text="New Saturation", command=self.new_sat_tree)
        self.new_sat_button.grid(row=2, column=1)
        self.new_val_button = Button(master=self.master, text="New Value", command=self.new_val_tree)
        self.new_val_button.grid(row=3, column=1)

        self.hue_shift = Scale(self.master, from_=0, to_=254, orient=HORIZONTAL, command=self.update_hue)
        self.hue_shift.grid(row=1, column=2, columnspan=2)
        self.hue_shift.set(self.preview.hsv_image.hue["shift"])
        self.sat_shift = Scale(self.master, from_=0, to_=254, orient=HORIZONTAL, command=self.update_sat)
        self.sat_shift.grid(row=2, column=2, columnspan=2)
        self.sat_shift.set(self.preview.hsv_image.sat["shift"])
        self.val_shift = Scale(self.master, from_=0, to_=254, orient=HORIZONTAL, command=self.update_val)
        self.val_shift.grid(row=3, column=2, columnspan=2)
        self.val_shift.set(self.preview.hsv_image.val["shift"])

        self.hue_range = Scale(self.master, from_=1, to_=256, orient=HORIZONTAL, command=self.update_hue)
        self.hue_range.grid(row=1, column=4, columnspan=2)
        self.hue_range.set(self.preview.hsv_image.hue["range"])
        self.sat_range = Scale(self.master, from_=1, to_=256, orient=HORIZONTAL, command=self.update_sat)
        self.sat_range.grid(row=2, column=4, columnspan=2)
        self.sat_range.set(self.preview.hsv_image.sat["range"])
        self.val_range = Scale(self.master, from_=1, to_=256, orient=HORIZONTAL, command=self.update_val)
        self.val_range.grid(row=3, column=4, columnspan=2)
        self.val_range.set(self.preview.hsv_image.val["range"])

        self.hue_visible = Button(master=self.master, text="Hide", command=self.toggle_hue)
        self.hue_visible.grid(row=1, column=6)
        self.sat_visible = Button(master=self.master, text="Hide", command=self.toggle_sat)
        self.sat_visible.grid(row=2, column=6)
        self.val_visible = Button(master=self.master, text="Hide", command=self.toggle_val)
        self.val_visible.grid(row=3, column=6)

        self.save_name = Entry(self.master)
        self.save_name.grid(row=4, column=0, columnspan=5)
        self.save_name.insert(0, "test")
        self.save_button = Button(master=self.master, text="Save", command=self.save)
        self.save_button.grid(row=4, column=6)

    def update_hue(self, n=None):
        self.preview.hsv_image.hue["range"] = self.hue_range.get()
        self.preview.hsv_image.hue["shift"] = self.hue_shift.get()
        self.preview._generate_hue_band()
        self.preview.update()

    def new_hue_tree(self):
        self.preview.hsv_image._new_hue()
        self.preview._generate_hue_band()
        self.preview.update()

    def update_sat(self, n=None):
        self.preview.hsv_image.sat["range"] = self.sat_range.get()
        self.preview.hsv_image.sat["shift"] = self.sat_shift.get()
        self.preview._generate_sat_band()
        self.preview.update()

    def new_sat_tree(self):
        self.preview.hsv_image._new_sat()
        self.preview._generate_sat_band()
        self.preview.update()

    def update_val(self, n=None):
        self.preview.hsv_image.val["range"] = self.val_range.get()
        self.preview.hsv_image.val["shift"] = self.val_shift.get()
        self.preview._generate_val_band()
        self.preview.update()

    def new_val_tree(self):
        self.preview.hsv_image._new_val()
        self.preview._generate_val_band()
        self.preview.update()

    def toggle_hue(self):
        self.preview.visibilities[0] = not self.preview.visibilities[0]
        text = "Hide" if self.preview.visibilities[0] else "Show"
        self.hue_visible.destroy()
        self.hue_visible = Button(self.master, text=text, command=self.toggle_hue)
        self.hue_visible.grid(row=1, column=6)
        self.preview.update()

    def toggle_sat(self):
        self.preview.visibilities[1] = not self.preview.visibilities[1]
        text = "Hide" if self.preview.visibilities[1] else "Show"
        self.sat_visible.destroy()
        self.sat_visible = Button(self.master, text=text, command=self.toggle_sat)
        self.sat_visible.grid(row=2, column=6)
        self.preview.update()

    def toggle_val(self):
        self.preview.visibilities[2] = not self.preview.visibilities[2]
        text = "Hide" if self.preview.visibilities[2] else "Show"
        self.val_visible.destroy()
        self.val_visible = Button(self.master, text=text, command=self.toggle_val)
        self.val_visible.grid(row=3, column=6)
        self.preview.update()

    def save(self):
        visibility = self.preview.visibilities
        color = self.preview.hsv_image.hue, self.preview.hsv_image.sat, self.preview.hsv_image.val
        bands = [generate_band(1200, 800, visibility[i], color[i]["tree"], color[i]["shift"], color[i]["range"]) for i in range(3)]

        final_image = PILImage.merge("HSV", bands).convert("RGB")
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


def save_HSV(width, height, name):
    hsv_image = HSVImage(width, height)
    color = hsv_image.hue, hsv_image.sat, hsv_image.val
    bands = [generate_band(width, height, True, color[i]["tree"], color[i]["shift"], color[i]["range"]) for i in range(3)]

    final_image = PILImage.merge("HSV", bands).convert("RGB")
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
        save_HSV(width, height, name)
