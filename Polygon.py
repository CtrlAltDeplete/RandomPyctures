import imageio
import math
import multiprocessing

from Functions import *
from os import remove
from PIL import Image as PILImage
from PIL import ImageDraw
from PIL import ImageTk
from random import randint
from sys import argv
from tkinter import *


class PolygonImage:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.polygon = {
            "sides": 6,
            "angles": [math.pi * randint(0, 359) / 180, math.pi * randint(0, 359) / 180,
                       math.pi * randint(0, 359) / 180, math.pi * randint(0, 359) / 180,
                       math.pi * randint(0, 359) / 180, math.pi * randint(0, 359) / 180],
            "distances": [randint(1, 100) / 100, randint(1, 100) / 100, randint(1, 100) / 100,
                          randint(1, 100) / 100, randint(1, 100) / 100, randint(1, 100) / 100]
        }
        self.polygon["angles"].sort()
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
        self.opac = {
            "tree": FunctionNode(0.6),
            "values": [],
            "shift": randint(0, 255),
            "range": randint(1, 256)
        }
        self.rot = {
            "tree": FunctionNode(0.6),
            "values": [],
            "shift": randint(0, 359),
            "range": randint(1, 360)
        }
        self.size = {
            "tree": FunctionNode(0.6),
            "values": [],
            "shift": randint(5, 50),
            "range": randint(5, 50)
        }
        self.step_size = 5
        self.generate()

    def generate(self):
        manager = multiprocessing.Manager()
        return_dict = manager.dict()

        jobs = []
        for func in (self._generate_hues, self._generate_sats, self._generate_vals, self._generate_opacs,
                     self._generate_rots, self._generate_sizes):
            p = multiprocessing.Process(target=func, args=(return_dict,))
            jobs.append(p)
            p.start()
        for proc in jobs:
            proc.join()

        self.hue["values"] = return_dict["hue"]
        self.sat["values"] = return_dict["sat"]
        self.val["values"] = return_dict["val"]
        self.opac["values"] = return_dict["opac"]
        self.rot["values"] = return_dict["rot"]
        self.size["values"] = return_dict["size"]

    def new_polygon(self):
        self.polygon = {
            "sides": 6,
            "angles": [math.pi * randint(0, 359) / 180, math.pi * randint(0, 359) / 180,
                       math.pi * randint(0, 359) / 180, math.pi * randint(0, 359) / 180,
                       math.pi * randint(0, 359) / 180, math.pi * randint(0, 359) / 180],
            "distances": [randint(1, 100) / 100, randint(1, 100) / 100, randint(1, 100) / 100,
                          randint(1, 100) / 100, randint(1, 100) / 100, randint(1, 100) / 100]
        }
        self.polygon["angles"].sort()

    def _generate_hues(self, return_dict=None):
        values = []
        for y in range(-self.step_size, self.height + self.step_size, self.step_size):
            adjusted_y = 2 * y / self.height
            for x in range(-self.step_size, self.width + self.step_size, self.step_size):
                adjusted_x = 2 * x / self.width
                values.append(self.hue["tree"].eval(adjusted_x, adjusted_y))
        if return_dict is not None:
            return_dict["hue"] = values
        else:
            self.hue["values"] = values

    def _generate_sats(self, return_dict=None):
        values = []
        for y in range(-self.step_size, self.height + self.step_size, self.step_size):
            adjusted_y = 2 * y / self.height
            for x in range(-self.step_size, self.width + self.step_size, self.step_size):
                adjusted_x = 2 * x / self.width
                values.append(self.sat["tree"].eval(adjusted_x, adjusted_y))
        if return_dict is not None:
            return_dict["sat"] = values
        else:
            self.sat["values"] = values

    def _generate_vals(self, return_dict=None):
        values = []
        for y in range(-self.step_size, self.height + self.step_size, self.step_size):
            adjusted_y = 2 * y / self.height
            for x in range(-self.step_size, self.width + self.step_size, self.step_size):
                adjusted_x = 2 * x / self.width
                values.append(self.val["tree"].eval(adjusted_x, adjusted_y))
        if return_dict is not None:
            return_dict["val"] = values
        else:
            self.val["values"] = values

    def _generate_opacs(self, return_dict=None):
        values = []
        for y in range(-self.step_size, self.height + self.step_size, self.step_size):
            adjusted_y = 2 * y / self.height
            for x in range(-self.step_size, self.width + self.step_size, self.step_size):
                adjusted_x = 2 * x / self.width
                values.append(self.opac["tree"].eval(adjusted_x, adjusted_y))
        if return_dict is not None:
            return_dict["opac"] = values
        else:
            self.opac["values"] = values

    def _generate_rots(self, return_dict=None):
        values = []
        for y in range(-self.step_size, self.height + self.step_size, self.step_size):
            adjusted_y = 2 * y / self.height
            for x in range(-self.step_size, self.width + self.step_size, self.step_size):
                adjusted_x = 2 * x / self.width
                values.append(self.rot["tree"].eval(adjusted_x, adjusted_y))
        if return_dict is not None:
            return_dict["rot"] = values
        else:
            self.rot["values"] = values

    def _generate_sizes(self, return_dict=None):
        values = []
        for y in range(-self.step_size, self.height + self.step_size, self.step_size):
            adjusted_y = 2 * y / self.height
            for x in range(-self.step_size, self.width + self.step_size, self.step_size):
                adjusted_x = 2 * x / self.width
                values.append(self.size["tree"].eval(adjusted_x, adjusted_y))
        if return_dict is not None:
            return_dict["size"] = values
        else:
            self.size["values"] = values

    def _new_hue(self, complexity=0.6):
        self.hue["tree"] = FunctionNode(complexity)
        self._generate_hues()

    def _new_sat(self, complexity=0.6):
        self.sat["tree"] = FunctionNode(complexity)
        self._generate_sats()

    def _new_val(self, complexity=0.6):
        self.val["tree"] = FunctionNode(complexity)
        self._generate_vals()

    def _new_opac(self, complexity=0.6):
        self.opac["tree"] = FunctionNode(complexity)
        self._generate_opacs()

    def _new_rot(self, complexity=0.6):
        self.rot["tree"] = FunctionNode(complexity)
        self._generate_rots()

    def _new_size(self, complexity=0.6):
        self.size["tree"] = FunctionNode(complexity)
        self._generate_sizes()

    def new(self, complexity=(0.6, 0.6, 0.6, 0.6, 0.6, 0.6)):
        self.hue["tree"] = FunctionNode(complexity[0])
        self.sat["tree"] = FunctionNode(complexity[1])
        self.val["tree"] = FunctionNode(complexity[2])
        self.opac["tree"] = FunctionNode(complexity[3])
        self.rot["tree"] = FunctionNode(complexity[4])
        self.size["tree"] = FunctionNode(complexity[5])
        self.generate()


class GUI:
    class Preview:
        def __init__(self, master):
            self.master = master
            self.frame = Frame(self.master)
            self.poly_image = PolygonImage(600, 400)
            self.pil_image = PILImage.new("RGB", (600, 400))
            self.draw = ImageDraw.Draw(self.pil_image, "RGBA")
            self.tk_image = ImageTk.PhotoImage(image=self.pil_image)
            self.label = Label(self.master, image=self.tk_image)
            self.label.pack()

        def update(self):
            self.draw.rectangle([0, 0, 600, 400], fill=(255, 255, 255))

            i = 0
            for y in range(-self.poly_image.step_size, 400 + self.poly_image.step_size, self.poly_image.step_size):
                for x in range(-self.poly_image.step_size, 600 + self.poly_image.step_size, self.poly_image.step_size):
                    generate_polygon(self.poly_image, self.draw, x, y, i)
                    i += 1

            self.tk_image = ImageTk.PhotoImage(image=self.pil_image)
            self.label.destroy()
            self.label = Label(self.master, image=self.tk_image)
            self.label.pack()

    def __init__(self, master):
        self.boot = True
        self.master = master
        self.frame = Frame(self.master)
        self.preview = self.Preview(Toplevel(self.master))

        Label(self.master, text="Tree").grid(row=0, column=1)
        Label(self.master, text="Shift").grid(row=0, column=2)
        Label(self.master, text="Range").grid(row=0, column=4)
        Label(self.master, text="Hue").grid(row=1, column=0)
        Label(self.master, text="Saturation").grid(row=2, column=0)
        Label(self.master, text="Value").grid(row=3, column=0)
        Label(self.master, text="Opacity").grid(row=4, column=0)
        Label(self.master, text="Rotation").grid(row=5, column=0)
        Label(self.master, text="Size").grid(row=6, column=0)

        self.new_hue_button = Button(master=self.master, text="New Hue", command=self.new_hue_tree)
        self.new_hue_button.grid(row=1, column=1)
        self.new_sat_button = Button(master=self.master, text="New Saturation", command=self.new_sat_tree)
        self.new_sat_button.grid(row=2, column=1)
        self.new_val_button = Button(master=self.master, text="New Value", command=self.new_val_tree)
        self.new_val_button.grid(row=3, column=1)
        self.new_opac_button = Button(master=self.master, text="New Opacity", command=self.new_opac_tree)
        self.new_opac_button.grid(row=4, column=1)
        self.new_rot_button = Button(master=self.master, text="New Rotation", command=self.new_rot_tree)
        self.new_rot_button.grid(row=5, column=1)
        self.new_size_button = Button(master=self.master, text="New Size", command=self.new_size_tree)
        self.new_size_button.grid(row=6, column=1)

        self.hue_shift = Scale(self.master, from_=0, to_=254, orient=HORIZONTAL, command=self.update)
        self.hue_shift.grid(row=1, column=2, columnspan=2)
        self.hue_shift.set(self.preview.poly_image.hue["shift"])
        self.sat_shift = Scale(self.master, from_=0, to_=254, orient=HORIZONTAL, command=self.update)
        self.sat_shift.grid(row=2, column=2, columnspan=2)
        self.sat_shift.set(self.preview.poly_image.sat["shift"])
        self.val_shift = Scale(self.master, from_=0, to_=254, orient=HORIZONTAL, command=self.update)
        self.val_shift.grid(row=3, column=2, columnspan=2)
        self.val_shift.set(self.preview.poly_image.val["shift"])
        self.opac_shift = Scale(self.master, from_=0, to_=254, orient=HORIZONTAL, command=self.update)
        self.opac_shift.grid(row=4, column=2, columnspan=2)
        self.opac_shift.set(self.preview.poly_image.opac["shift"])
        self.rot_shift = Scale(self.master, from_=0, to_=359, orient=HORIZONTAL, command=self.update)
        self.rot_shift.grid(row=5, column=2, columnspan=2)
        self.rot_shift.set(self.preview.poly_image.rot["shift"])
        self.size_shift = Scale(self.master, from_=5, to_=50, orient=HORIZONTAL, command=self.update)
        self.size_shift.grid(row=6, column=2, columnspan=2)
        self.size_shift.set(self.preview.poly_image.size["shift"])

        self.hue_range = Scale(self.master, from_=1, to_=256, orient=HORIZONTAL, command=self.update)
        self.hue_range.grid(row=1, column=4, columnspan=2)
        self.hue_range.set(self.preview.poly_image.hue["range"])
        self.sat_range = Scale(self.master, from_=1, to_=256, orient=HORIZONTAL, command=self.update)
        self.sat_range.grid(row=2, column=4, columnspan=2)
        self.sat_range.set(self.preview.poly_image.sat["range"])
        self.val_range = Scale(self.master, from_=1, to_=256, orient=HORIZONTAL, command=self.update)
        self.val_range.grid(row=3, column=4, columnspan=2)
        self.val_range.set(self.preview.poly_image.val["range"])
        self.opac_range = Scale(self.master, from_=1, to_=256, orient=HORIZONTAL, command=self.update)
        self.opac_range.grid(row=4, column=4, columnspan=2)
        self.opac_range.set(self.preview.poly_image.opac["range"])
        self.rot_range = Scale(self.master, from_=1, to_=360, orient=HORIZONTAL, command=self.update)
        self.rot_range.grid(row=5, column=4, columnspan=2)
        self.rot_range.set(self.preview.poly_image.rot["range"])
        self.size_range = Scale(self.master, from_=1, to_=50, orient=HORIZONTAL, command=self.update)
        self.size_range.grid(row=6, column=4, columnspan=2)
        self.size_range.set(self.preview.poly_image.size["range"])

        self.step_size = IntVar(master=self.master, value=self.preview.poly_image.step_size)
        self.step_size_entry = Entry(master=self.master, textvariable=self.step_size)
        self.step_size_update = Button(self.master, text="Update", command=self.update_step_size)
        Label(self.master, text="Step Size").grid(row=7, column=0)
        self.step_size_entry.grid(row=7, column=1, columnspan=3)
        self.step_size_update.grid(row=7, column=4)

        self.polygon_canvas = Canvas(self.master, width=32, height=32)
        self.polygon_canvas.grid(row=8, column=1)
        self.new_polygon_btn = Button(self.master, text="New Polygon", command=self.new_polygon)
        self.new_polygon_btn.grid(row=8, column=0)
        points = []
        for i in range(6):
            x = 16 + 16 * self.preview.poly_image.polygon["distances"][i] * \
                math.cos(self.preview.poly_image.polygon["angles"][i])
            y = 16 + 16 * self.preview.poly_image.polygon["distances"][i] * \
                math.sin(self.preview.poly_image.polygon["angles"][i])
            points.append((x, y))
        self.polygon_canvas.create_polygon(points, fill="black")

        self.gif_button = Button(self.master, text="Create GIF", command=self.create_gif)
        self.gif_button.grid(row=9, column=5)

        self.save_name = Entry(self.master)
        self.save_name.grid(row=9, column=1, columnspan=3)
        self.save_name.insert(0, "test")
        self.save_button = Button(master=self.master, text="Save", command=self.save)
        self.save_button.grid(row=9, column=4)

        self.boot = False
        self.update()

    def update(self, n=None):
        if not self.boot:
            self.preview.poly_image.hue["range"] = self.hue_range.get()
            self.preview.poly_image.hue["shift"] = self.hue_shift.get()
            self.preview.poly_image.sat["range"] = self.sat_range.get()
            self.preview.poly_image.sat["shift"] = self.sat_shift.get()
            self.preview.poly_image.val["range"] = self.val_range.get()
            self.preview.poly_image.val["shift"] = self.val_shift.get()
            self.preview.poly_image.opac["range"] = self.opac_range.get()
            self.preview.poly_image.opac["shift"] = self.opac_shift.get()
            self.preview.poly_image.rot["range"] = self.rot_range.get()
            self.preview.poly_image.rot["shift"] = self.rot_shift.get()
            self.preview.poly_image.size["range"] = self.size_range.get()
            self.preview.poly_image.size["shift"] = self.size_shift.get()
            self.preview.update()

    def update_step_size(self):
        if not self.boot:
            try:
                self.preview.poly_image.step_size = self.step_size.get()
                self.preview.poly_image.generate()
                self.update()
            except TclError:
                pass

    def new_polygon(self):
        self.polygon_canvas.destroy()
        self.polygon_canvas = Canvas(self.master, width=32, height=32)
        self.polygon_canvas.grid(row=8, column=1)
        self.preview.poly_image.new_polygon()
        points = []
        for i in range(6):
            x = 16 + 16 * self.preview.poly_image.polygon["distances"][i] * \
                math.cos(self.preview.poly_image.polygon["angles"][i])
            y = 16 + 16 * self.preview.poly_image.polygon["distances"][i] * \
                math.sin(self.preview.poly_image.polygon["angles"][i])
            points.append((x, y))
        self.polygon_canvas.create_polygon(points, fill="black")
        self.preview.update()

    def new_hue_tree(self):
        self.preview.poly_image._new_hue()
        self.preview.update()

    def new_sat_tree(self):
        self.preview.poly_image._new_sat()
        self.preview.update()

    def new_val_tree(self):
        self.preview.poly_image._new_val()
        self.preview.update()

    def new_opac_tree(self):
        self.preview.poly_image._new_opac()
        self.preview.update()

    def new_rot_tree(self):
        self.preview.poly_image._new_rot()
        self.preview.update()

    def new_size_tree(self):
        self.preview.poly_image._new_size()
        self.preview.update()

    def save(self):
        self.preview.pil_image.save(self.save_name.get() + ".png", "PNG")

    def create_gif(self):
        frames = []
        for i in range(0, 360):
            self.preview.poly_image.rot["shift"] = i
            self.preview.update()
            self.preview.pil_image.save("{}-{}.png".format(self.save_name.get(), i))
            frames.append(imageio.imread("{}-{}.png".format(self.save_name.get(), i)))
        imageio.mimsave('{}.gif'.format(self.save_name.get()), frames, 'GIF', duration=1/60)
        for i in range(0, 360):
            remove("{}-{}.png".format(self.save_name.get(), i))


def hsv_to_rgb(h, s, v):
    h = 360 * h / 255
    s = s / 255
    v = v / 255
    c = v * s
    x = c * (1 - abs(h / 60 % 2 - 1))
    m = v - c
    if h < 60:
        r, g, b = c, x, 0
    elif h < 120:
        r, g, b = x, c, 0
    elif h < 180:
        r, g, b = 0, c, x
    elif h < 240:
        r, g, b = 0, x, c
    elif h < 300:
        r, g, b = x, 0, c
    else:
        r, g, b = c, 0, x
    return int((r + m) * 255), int((g + m) * 255), int((b + m) * 255)


def generate_polygon(poly_image, draw, x, y, i):
    hue = (poly_image.hue["range"] * (poly_image.hue["values"][i] / 2 + 0.5) + poly_image.hue["shift"]) % 255
    sat = (poly_image.sat["range"] * (poly_image.sat["values"][i] / 2 + 0.5) +
           poly_image.sat["shift"]) % 255
    val = (poly_image.val["range"] * (poly_image.val["values"][i] / 2 + 0.5) +
           poly_image.val["shift"]) % 255
    opac = (poly_image.opac["range"] * (poly_image.opac["values"][i] / 2 + 0.5) +
            poly_image.opac["shift"]) % 255
    rot = math.pi * ((poly_image.rot["range"] * (poly_image.rot["values"][i] / 2 + 0.5) +
                      poly_image.rot["shift"]) % 360) / 180
    size = poly_image.size["range"] * (poly_image.size["values"][i] / 2 + 0.5) + \
           poly_image.size["shift"]

    red, green, blue = hsv_to_rgb(hue, sat, val)
    angles = [rot + theta for theta in poly_image.polygon["angles"]]
    distances = [size * dist for dist in poly_image.polygon["distances"]]
    points = []
    for j in range(len(angles)):
        points.append((
            x + distances[j] * math.cos(angles[j]),
            y + distances[j] * math.sin(angles[j])
        ))
    draw.polygon(points, fill=(red, green, blue, int(opac)))


def save_polygon_png(width, height, name):
    poly_image = PolygonImage(width, height)
    pil_image = PILImage.new("RGB", (width, height))
    draw = ImageDraw.Draw(pil_image, "RGBA")

    draw.rectangle([0, 0, width, height], fill=(255, 255, 255))
    i = 0
    for y in range(-poly_image.step_size, height + poly_image.step_size, poly_image.step_size):
        for x in range(-poly_image.step_size, width + poly_image.step_size, poly_image.step_size):
            generate_polygon(poly_image, draw, x, y, i)
            i += 1
    pil_image.save(name + ".png", "PNG")


def save_polygon_gif(width, height, name):
    poly_image = PolygonImage(width, height)
    pil_image = PILImage.new("RGB", (width, height))
    draw = ImageDraw.Draw(pil_image, "RGBA")

    frames = []
    for j in range(0, 360):
        poly_image.rot["shift"] = j
        draw.rectangle([0, 0, width, height], fill=(255, 255, 255))
        i = 0
        for y in range(-poly_image.step_size, height + poly_image.step_size, poly_image.step_size):
            for x in range(-poly_image.step_size, width + poly_image.step_size, poly_image.step_size):
                generate_polygon(poly_image, draw, x, y, i)
                i += 1
        pil_image.save("{}-{}.png".format(name, j), "PNG")
        frames.append(imageio.imread("{}-{}.png".format(name, j)))

    imageio.mimsave('{}.gif'.format(name), frames, 'GIF', duration=1/60)
    for i in range(0, 360):
        remove("{}-{}.png".format(name, i))


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
        if "-gif" in argv:
            save_polygon_gif(width, height, name)
        else:
            save_polygon_png(width, height, name)
