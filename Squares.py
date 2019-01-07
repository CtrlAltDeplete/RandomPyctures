import math
import multiprocessing

from Functions import *
from PIL import Image as PILImage
from PIL import ImageDraw
from random import randint
from random import seed


class SquaresImage:
    def __init__(self, width, height, box_size):
        self.width = width
        self.height = height
        self.box_size = box_size
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
        for y in range(0, self.height, self.box_size):
            adjusted_y = 2 * y / self.height - 1
            for x in range(0, self.width, self.box_size):
                adjusted_x = 2 * x / self.width - 1
                values.append((self.red["tree"].eval(adjusted_x, adjusted_y) + 1) * self.red["range"] / 2 + self.red["shift"] % 255)
        if return_dict is not None:
            return_dict["red"] = values
        else:
            self.red["values"] = values

    def _generate_greens(self, return_dict=None):
        values = []
        for y in range(0, self.height, self.box_size):
            adjusted_y = 2 * y / self.height - 1
            for x in range(0, self.width, self.box_size):
                adjusted_x = 2 * x / self.width - 1
                values.append((self.green["tree"].eval(adjusted_x, adjusted_y) + 1) * self.green["range"] / 2 + self.green["shift"] % 255)
        if return_dict is not None:
            return_dict["green"] = values
        else:
            self.green["values"] = values

    def _generate_blues(self, return_dict=None):
        values = []
        for y in range(0, self.height, self.box_size):
            adjusted_y = 2 * y / self.height - 1
            for x in range(0, self.width, self.box_size):
                adjusted_x = 2 * x / self.width - 1
                values.append((self.blue["tree"].eval(adjusted_x, adjusted_y) + 1) * self.blue["range"] / 2 + self.blue["shift"] % 255)
        if return_dict is not None:
            return_dict["blue"] = values
        else:
            self.blue["values"] = values


def create_b_curve(points, t):
    b_curve = []
    for i in range(1, t + 1):
        c = i / t
        x = 0
        y = 0
        for n in range(len(points)):
            coefs = [math.factorial(len(points) - 1) / (math.factorial(len(points) - 1 - n) * math.factorial(n)),
                     (1 - c) ** (len(points) - 1 - n), c ** n]
            x += coefs[0] * coefs[1] * coefs[2] * points[n][0]
            y += coefs[0] * coefs[1] * coefs[2] * points[n][1]
        b_curve.append((x, y))
    return b_curve


def draw_polygon(draw, points, outline, width):
    for i in range(len(points) - 1):
        draw.line([points[i], points[i + 1]], fill=outline, width=width)
    draw.line([points[-1], points[0]], fill=outline, width=width)


def draw_squares(x, y, box_width, box_height, color, t, draw):
    middle_squares = [(x + randint(0, box_width // 2), y + randint(0, box_height // 2)),
                      (x + randint(box_width // 2, box_width), y + randint(0, box_height // 2)),
                      (x + randint(box_width // 2, box_width), y + randint(box_height // 2, box_height)),
                      (x + randint(0, box_width // 2), y + randint(box_height // 2, box_height))]
    points = [create_b_curve([(x, y), middle_squares[0], (x + box_width // 2, y + box_height // 2)], t),
              create_b_curve([(x + box_width, y), middle_squares[1], (x + box_width // 2, y + box_height // 2)], t),
              create_b_curve([(x + box_width, y + box_height), middle_squares[2], (x + box_width // 2, y + box_height // 2)], t),
              create_b_curve([(x, y + box_height), middle_squares[3], (x + box_width // 2, y + box_height // 2)], t)]
    outline = color[0], color[1], color[2], 255
    fill = color[0], color[1], color[2], 48
    draw.rectangle([x, y, x + box_width - 1, y + box_height - 1], fill=fill)
    for i in range(t):
        draw_polygon(draw, [points[0][i], points[1][i], points[2][i], points[3][i]], outline, 3)


def draw_lines(x, y, box_size, color, draw):
    fill = color[0], color[1], color[2], 48
    outline = color[0], color[1], color[2], 224
    draw.rectangle([x, y, x + box_size - 1, y + box_size - 1], fill=fill)
    for i in range(box_size):
        center = randint(x, x + box_size), randint(y, y + box_size)
        length = randint(box_size // 4, box_size // 2)
        theta = randint(0, 360) * math.pi / 180
        p1 = center[0] + math.cos(theta) * length / 2, center[1] + math.sin(theta) * length / 2
        p2 = center[0] - math.cos(theta) * length / 2, center[1] - math.sin(theta) * length / 2
        draw.line([p1, p2], fill=outline)


def section_image_into_grids(width, height, draw):
    y = 0
    x = 0
    while y < height - randint(40, 100):
        y += randint(40, 100)
        draw.line([0, y, width, y], fill=(0, 0, 0, 255))
    while x < width - randint(40, 100):
        x += randint(40, 100)
        draw.line([x, 0, x, height], fill=(0, 0, 0, 255))


def color_sections(width, height, square, img, draw):
    sections = []
    start_x, start_y = 0, 0
    x, y = 0, 0
    while start_x != width or start_y != height:
        while x < width and img.getpixel((x, y)) == (255, 255, 255):
            x += 1
        x -= 1
        while y < height and img.getpixel((x, y)) == (255, 255, 255):
            y += 1
        y -= 1
        sections.append(((start_x, start_y), (x + 1, y + 1)))
        if x == width - 1 and y == height - 1:
            start_x = width
            start_y = height
        elif x == width - 1:
            x = 0
            start_x = x
            y += 2
            start_y = y
        else:
            x += 2
            start_x = x
            y = start_y
    draw.rectangle((0, 0, width, height), fill=(255, 255, 255, 255))
    for section in sections:
        x, y = section[0]
        width = section[1][0] - x + 1
        height = section[1][1] - y + 1
        t = min(width, height) // 12
        new_x = 2 * x / width - 1
        new_y = 2 * y / width - 1
        color = (
            int((square.red["tree"].eval(new_x, new_y) / 2 + 0.5) * square.red["range"] + square.red["shift"] % 256),
            int((square.green["tree"].eval(new_x, new_y) / 2 + 0.5) * square.green["range"] + square.green["shift"] % 256),
            int((square.blue["tree"].eval(new_x, new_y) / 2 + 0.5) * square.blue["range"] + square.blue["shift"] % 256)
        )
        draw_squares(x, y, width, height, color, t, draw)


def save(box_size):
    img = PILImage.new("RGB", (1200, 800), color="white")
    draw = ImageDraw.ImageDraw(img, "RGBA")
    square = SquaresImage(1200, 800, box_size)
    # i = 0
    # for y in range(0, 800, box_size):
    #     for x in range(0, 1200, box_size):
    #         red = int(square.red["values"][i])
    #         green = int(square.green["values"][i])
    #         blue = int(square.blue["values"][i])
    #         draw_squares(x, y, box_size, (red, green, blue), draw)
    #         i += 1
    section_image_into_grids(1200, 800, draw)
    color_sections(1200, 800, square, img, draw)
    img.save("test.png", "PNG")


if __name__ == "__main__":
    save(50)
