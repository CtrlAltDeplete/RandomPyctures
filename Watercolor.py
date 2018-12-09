import math

from PIL import Image as PILImage
from PIL import ImageDraw
from PIL import ImageTk
from random import choice
from random import randint
from sys import argv
from tkinter import *


class WatercolorImage:
    def __init__(self, width, height, blobs=None, strokes=None):
        self.width = width
        self.height = height
        if strokes:
            self.strokes = strokes
        else:
            self.strokes = {
                "count": randint(60, 90),
                "size": (10, 55),
                "values": []
            }
        if blobs:
            self.blobs = blobs
        else:
            self.blobs = {
                "count": randint(80, 120),
                "size": (30, 70),
                "values": []
            }
        self.strokes["values"] = [self.generate_stroke() for i in range(self.strokes["count"])]
        self.blobs["values"] = [self.generate_blob() for i in range(self.blobs["count"])]

    def generate_stroke(self):
        def calc_perp(p1, p2, upper=False):
            def calc_angle():
                dx = p2[0] - p1[0]
                dy = p2[1] - p1[1]
                quad = 1
                if dx < 0:
                    if dy < 0:
                        quad = 3
                    else:
                        quad = 2
                else:
                    if dy < 0:
                        quad = 4
                try:
                    angle = math.atan(dy / dx)
                    if quad == 2:
                        angle += math.pi
                    elif quad == 3:
                        angle = math.pi + angle
                except ZeroDivisionError:
                    if dy > 0:
                        angle = math.pi / 2
                    else:
                        angle = 3 * math.pi / 2
                while angle < 0 or angle >= 2 * math.pi:
                    angle += (math.pi * 2)
                    angle %= (math.pi * 2)
                return angle

            if upper:
                angle = calc_angle() + math.pi / 2
            else:
                angle = calc_angle() - math.pi / 2
            while angle < 0 or angle >= 2 * math.pi:
                angle += (math.pi * 2)
                angle %= (math.pi * 2)
            return angle

        points = []
        num_points = randint(3, 7)
        for i in range(num_points):
            x = randint(-self.width // 4, self.width * 5 // 4)
            y = randint(-self.height // 4, self.height * 5 // 4)
            points.append((x, y))
        if randint(0, 10) < 5:
            points.sort(key=lambda point: point[0])
        else:
            points.sort(key=lambda point: point[1])
        b_curve = []
        for i in range(12):
            t = i / 11
            x = 0
            y = 0
            for n in range(len(points)):
                coefs = [math.factorial(len(points) - 1) / (math.factorial(len(points) - 1 - n) * math.factorial(n)),
                         (1 - t) ** (len(points) - 1 - n), t ** n]
                x += coefs[0] * coefs[1] * coefs[2] * points[n][0]
                y += coefs[0] * coefs[1] * coefs[2] * points[n][1]
            b_curve.append((x, y))

        stroke_points = []
        size = randint(self.strokes["size"][0], self.strokes["size"][1])
        # Draw the rounded beginning, starting with the upper perp
        angle = calc_perp(b_curve[0], b_curve[1]) + math.pi
        for i in range(4):
            x = b_curve[0][0] + size * math.cos(angle)
            y = b_curve[0][1] + size * math.sin(angle)
            stroke_points.append((x, y))
            angle += math.pi / 3
        # Draw the lower perp for each mid point
        for i in range(1, len(b_curve) - 1):
            angle = calc_perp(b_curve[i - 1], b_curve[i + 1], False) + math.pi
            x = b_curve[i][0] + size * math.cos(angle)
            y = b_curve[i][1] + size * math.sin(angle)
            stroke_points.append((x, y))
        # Draw the rounded end, starting with the lower perp
        angle = calc_perp(b_curve[-2], b_curve[-1], False)
        for i in range(4):
            x = b_curve[-1][0] + size * math.cos(angle)
            y = b_curve[-1][1] + size * math.sin(angle)
            stroke_points.append((x, y))
            angle += math.pi / 3
        # Draw the upper perp for each mid point
        for i in range(1, len(b_curve) - 1):
            angle = calc_perp(b_curve[-2 - i], b_curve[-i])
            x = b_curve[-1 - i][0] + size * math.cos(angle)
            y = b_curve[-1 - i][1] + size * math.sin(angle)
            stroke_points.append((x, y))
        return stroke_points

    def generate_blob(self):
        blob_points = []
        x, y = randint(0, self.width), randint(0, self.height)
        size = randint(self.blobs["size"][0], self.blobs["size"][1])
        angle = randint(0, 359) * math.pi / 180
        num_points = randint(5, 9)
        for i in range(num_points):
            blob_points.append((x + math.cos(angle) * size, y + math.sin(angle) * size))
            angle += 2 * math.pi / num_points
        return blob_points


class GUI:
    class Preview:
        def __init__(self, master):
            self.master = master
            self.frame = Frame(self.master)
            self.pil_image = PILImage.new("RGB", (600, 400))
            self.draw = ImageDraw.Draw(self.pil_image, "RGBA")
            self.watercolor = None
            self.colors = None
            self.tk_image = None
            self.label = None
            self.new()

        def new(self, retain=False):
            if retain:
                strokes = self.watercolor.strokes
                blobs = self.watercolor.blobs
                strokes["values"] = []
                blobs["values"] = []
                self.watercolor = WatercolorImage(600, 400, strokes, blobs)
            else:
                self.watercolor = WatercolorImage(600, 400)
            self.colors = [(randint(0, 255), randint(0, 255), randint(0, 255), 8),
                           (randint(0, 255), randint(0, 255), randint(0, 255), 8),
                           (randint(0, 255), randint(0, 255), randint(0, 255), 8),
                           (randint(0, 255), randint(0, 255), randint(0, 255), 8)]
            self.draw.rectangle([0, 0, 600, 400], fill="white")
            all_polys = self.watercolor.strokes["values"].copy()
            all_polys.extend(self.watercolor.blobs["values"])
            for poly in all_polys:
                paint_polygon(self.watercolor, poly, choice(self.colors), self.draw)
            self.tk_image = ImageTk.PhotoImage(image=self.pil_image)
            if self.label:
                self.label.destroy()
            self.label = Label(self.master, image=self.tk_image)
            self.label.pack()

    def __init__(self, master):
        self.master = master
        self.frame = Frame(self.master)
        self.preview = self.Preview(Toplevel(self.master))

        Label(self.master, text="Min Size").grid(row=0, column=1)
        Label(self.master, text="Max Size").grid(row=0, column=3)
        Label(self.master, text="Count").grid(row=0, column=5)
        Label(self.master, text="Strokes").grid(row=1, column=0)
        Label(self.master, text="Blobs").grid(row=2, column=0)

        self.stroke_min_size = Entry(self.master)
        self.stroke_max_size = Entry(self.master)
        self.stroke_count = Entry(self.master)
        self.stroke_min_size.grid(row=1, column=1, columnspan=2)
        self.stroke_max_size.grid(row=1, column=3, columnspan=2)
        self.stroke_count.grid(row=1, column=5, columnspan=2)
        self.stroke_min_size.insert(0, str(self.preview.watercolor.strokes["size"][0]))
        self.stroke_max_size.insert(0, str(self.preview.watercolor.strokes["size"][1]))
        self.stroke_count.insert(0, str(self.preview.watercolor.strokes["count"]))

        self.blob_min_size = Entry(self.master)
        self.blob_max_size = Entry(self.master)
        self.blob_count = Entry(self.master)
        self.blob_min_size.grid(row=2, column=1, columnspan=2)
        self.blob_max_size.grid(row=2, column=3, columnspan=2)
        self.blob_count.grid(row=2, column=5, columnspan=2)
        self.blob_min_size.insert(0, str(self.preview.watercolor.blobs["size"][0]))
        self.blob_max_size.insert(0, str(self.preview.watercolor.blobs["size"][1]))
        self.blob_count.insert(0, str(self.preview.watercolor.blobs["count"]))

        self.new_button = Button(self.master, text="New", command=self.preview.new)
        self.new_button.grid(row=3, column=0)

        self.update_button = Button(self.master, text="Update", command=self.update)
        self.update_button.grid(row=3, column=1)

        self.save_name = Entry(self.master)
        self.save_name.grid(row=3, column=3, columnspan=2)
        self.save_name.insert(0, "test")
        self.save_button = Button(master=self.master, text="Save", command=self.save)
        self.save_button.grid(row=3, column=5)

    def update(self):
        self.preview.watercolor.strokes["size"] = (int(self.stroke_min_size.get()), int(self.stroke_max_size.get()))
        self.preview.watercolor.strokes["count"] = int(self.stroke_count.get())
        self.preview.watercolor.blobs["size"] = (int(self.blob_min_size.get()), int(self.blob_max_size.get()))
        self.preview.watercolor.blobs["count"] = int(self.blob_count.get())
        self.preview.new(True)

    def save(self):
        self.preview.pil_image.save(self.save_name.get() + ".png", "PNG")


def deform_polygon(poly):
    def rand_point():
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        try:
            x = dx / abs(dx) * randint(0, int(abs(dx)))
        except ZeroDivisionError:
            x = 0
        try:
            y = dy / abs(dy) * randint(0, int(abs(dy)))
        except ZeroDivisionError:
            y = 0
        return p1[0] + x, p1[1] + y

    new_poly = []
    for i in range(len(poly)):
        p1 = poly[i]
        if len(poly) - 1 == i:
            p2 = poly[0]
            new_poly.append(p1)
        else:
            p2 = poly[i + 1]
        new_poly.append(rand_point())
        new_poly.append(p2)
    return new_poly


def paint_polygon(watercolor, polygon, color, draw):
    for i in range(randint(watercolor.strokes["size"][0] // 20, watercolor.strokes["size"][1] // 12)):
        poly = polygon
        for j in range(randint(watercolor.strokes["size"][0] // 11, watercolor.strokes["size"][1] // 9)):
            poly = deform_polygon(poly)
        draw.polygon(poly, fill=color)


def save_watercolor(name, width, height, blobs, strokes):
    if not width or not height:
        width = 1200
        height = 800
    if not name:
        name = "test"
    watercolor = WatercolorImage(width, height, blobs, strokes)
    pil_image = PILImage.new("RGB", (width, height))
    draw = ImageDraw.Draw(pil_image, "RGBA")
    colors = [(randint(0, 255), randint(0, 255), randint(0, 255), 8),
              (randint(0, 255), randint(0, 255), randint(0, 255), 8),
              (randint(0, 255), randint(0, 255), randint(0, 255), 8),
              (randint(0, 255), randint(0, 255), randint(0, 255), 8)]
    draw.rectangle([0, 0, width, height], fill="white")
    all_polys = watercolor.strokes["values"].copy()
    all_polys.extend(watercolor.blobs["values"])
    for poly in all_polys:
        paint_polygon(watercolor, poly, choice(colors), draw)
    pil_image.save(name + ".png", "PNG")


if __name__ == "__main__":
    if "-gui" in argv:
        root = Tk()
        gui = GUI(root)
        root.mainloop()
    else:
        width = None
        height = None
        name = None
        if "-size" in argv:
            index = argv.index("-size")
            width = int(argv[index + 1])
            height = int(argv[index + 2])
        if "-name" in argv:
            name = argv[argv.index("-name") + 1]
        if "-blob_count" in argv:
            blob_count = int(argv[argv.index("-blob_count") + 1])
        else:
            blob_count = randint(80, 120)
        if "-blob_size" in argv:
            blob_min = int(argv[argv.index("-blob_size") + 1])
            blob_max = int(argv[argv.index("-blob_size") + 2])
        else:
            blob_min, blob_max = 30, 70
        if "-stroke_count" in argv:
            stroke_count = int(argv[argv.index("-stroke_count") + 1])
        else:
            stroke_count = randint(60, 90)
        if "-stroke_size" in argv:
            stroke_min = int(argv[argv.index("-stroke_size") + 1])
            stroke_max = int(argv[argv.index("-stroke_size") + 2])
        else:
            stroke_min, stroke_max = 10, 55
        blobs = {
            "count": blob_count,
            "size": (blob_min, blob_max),
            "values": []
        }
        strokes = {
            "count": stroke_count,
            "size": (stroke_min, stroke_max),
            "values": []
        }
        save_watercolor(name, width, height, blobs, strokes)
