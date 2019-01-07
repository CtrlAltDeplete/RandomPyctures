from random import choice
from random import random
from math import *
from scipy import special


class Function:
    '''This is the parent class for all functions used.'''
    def __init__(self):
        '''When a function is made, it will randomly be assigned a
        delta x and y to make sure everything is not centered.
        Additionally, the input of the function will be [-1, 1],
        and the output of the function needs to be [-1, 1].'''
        self.dx = random() * choice([1, -1]) / 4
        self.dy = random() * choice([1, -1]) / 4
        self.cx = random() * choice([1, -1]) + 1
        self.cy = random() * choice([1, -1]) + 1
        self.zmin = self.eval(1, 1, False)
        self.zmax = self.zmin
        # To constrict output between -1 and 1, we calclate the max
        # And min output with inputs between -1 and 1, and manipulate
        # The output accordingly.
        for ix in range(-100, 100):
            for iy in range(-100, 100):
                z = self.eval(ix / 100, iy / 100, False)
                self.zmin = min(self.zmin, z)
                self.zmax = max(self.zmax, z)

    def eval(self, x, y, normalized=True):
        return

    def __str__(self):
        return str(type(self))[18:-2]


class X(Function):
    def __init__(self):
        pass

    def eval(self, x, y, normalized=True):
        return x

    # def __str__(self):
    #     return "x"


class Y(Function):
    def __init__(self):
        pass

    def eval(self, x, y, normalized=True):
        return y

    # def __str__(self):
    #     return "y"


class InverseX(Function):
    def eval(self, x, y, normalized=True):
        newX = x * self.cx + self.dx
        z = -1 * newX
        if normalized:
            return map_to(z, self.zmin, self.zmax, -1, 1)
        return z

    # def __str__(self):
    #     return "-1 * (x * {} + {})".format(self.cx, self.dx)


class InverseY(Function):
    def eval(self, x, y, normalized=True):
        newY = y * self.cy + self.dy
        z = -1 * newY
        if normalized:
            return map_to(z, self.zmin, self.zmax, -1, 1)
        return z

    # def __str__(self):
    #     return "-1 * (y * {} + {})".format(self.cy, self.dy)


class Ripple(Function):
    def eval(self, x, y, normalized=True):
        newX = x * self.cx + self.dx
        newY = y * self.cy + self.dy
        z = newX * newY ** 3 - newY * newX ** 3
        if normalized:
            z = max(self.zmin, min(self.zmax, z))
            return map_to(z, self.zmin, self.zmax, -1, 1)
        return z

    # def __str__(self):
    #     return "(x * {} + {}) * (y * {} + {}) ** 3 - (y * {} + {}) * (x * {} + {}) ** 3".format(self.cx, self.dx,
    #                                                                                             self.cy, self.dy,
    #                                                                                             self.cy, self.dy,
    #                                                                                             self.cx, self.dx)


class Sinkhole(Function):
    def eval(self, x, y, normalized=True):
        newX = x * self.cx + self.dx
        newY = y * self.cy + self.dy
        z = (newX ** 2 + newY ** 2) * e ** (-newX ** 2 - newY ** 2)
        if normalized:
            z = max(self.zmin, min(self.zmax, z))
            return map_to(z, self.zmin, self.zmax, -1, 1)
        return z

    # def __str__(self):
    #     return "((x * {} + {}) ** 2 + (y * {} + {}) ** 2) * e ** (-(x * {} + {}) ** 2 - (y * {} + {}) ** 2)".format(
    #         self.cx, self.dx, self.cy, self.dy, self.cx, self.dx, self.cy, self.dy
    #     )


class Pulse(Function):
    def eval(self, x, y, normalized=True):
        newX = x * self.cx + self.dx
        newY = y * self.cy + self.dy
        z = -newX * newY * e ** (-newX ** 2 - newY ** 2)
        if normalized:
            z = max(self.zmin, min(self.zmax, z))
            return map_to(z, self.zmin, self.zmax, -1, 1)
        return z

    # def __str__(self):
    #     return "-(x * {} + {}) * (y * {} + {}) ** 2) * e ** (-(x * {} + {}) ** 2 - (y * {} + {}) ** 2) ** 2)".format(
    #         self.cx, self.dx, self.cy, self.dy, self.cx, self.dx, self.cy, self.dy
    #     )


class Hill(Function):
    def eval(self, x, y, normalized=True):
        newX = x * self.cx + self.dx
        newY = y * self.cy + self.dy
        z = cos(abs(newX) + abs(newY))
        if normalized:
            z = max(self.zmin, min(self.zmax, z))
            return map_to(z, self.zmin, self.zmax, -1, 1)
        return z

    # def __str__(self):
    #     return "cos(abs((x * {} + {})) + abs((y * {} + {})))".format(self.cx, self.dx, self.cy, self.dy)


class Sinkhole2(Function):
    def eval(self, x, y, normalized=True):
        newX = x * self.cx + self.dx
        newY = y * self.cy + self.dy
        z = cos(abs(newX) + abs(newY)) * (abs(newX) + abs(newY))
        if normalized:
            z = max(self.zmin, min(self.zmax, z))
            return map_to(z, self.zmin, self.zmax, -1, 1)
        return z

    # def __str__(self):
    #     return "cos(abs((x * {} + {})) + abs((y * {} + {}))) * (abs((x * {} + {})) + abs((y * {} + {})))".format(
    #         self.cx, self.dx, self.cy, self.dy, self.cx, self.dx, self.cy, self.dy
    #     )


class Ripple2(Function):
    def eval(self, x, y, normalized=True):
        newX = x * self.cx + self.dx
        newY = y * self.cy + self.dy
        z = newX ** 3 - newX + newY ** 3 * newY
        if normalized:
            z = max(self.zmin, min(self.zmax, z))
            return map_to(z, self.zmin, self.zmax, -1, 1)
        return z

    # def __str__(self):
    #     return "(x * {} + {}) ** 3 - (x * {} + {}) + (y * {} + {}) ** 3 * (y * {} + {})".format(
    #         self.cx, self.dx, self.cx, self.dx, self.cy, self.dy, self.cy, self.dy
    #     )


class Bendy(Function):
    def eval(self, x, y, normalized=True):
        newX = x * self.cx + self.dx
        newY = y * self.cy + self.dy
        z = sin(newX * newY)
        if normalized:
            z = max(self.zmin, min(self.zmax, z))
            return map_to(z, self.zmin, self.zmax, -1, 1)
        return z

    # def __str__(self):
    #     return "sin((x * {} + {}) * (y * {} + {}))".format(self.cx, self.dx, self.cy, self.dy)


class Checkered(Function):
    def eval(self, x, y, normalized=True):
        newX = x * self.cx + self.dx
        newY = y * self.cy + self.dy
        z = sin(cos(tan(newX))) * sin(cos(tan(newY)))
        if normalized:
            z = max(self.zmin, min(self.zmax, z))
            return map_to(z, self.zmin, self.zmax, -1, 1)
        return z

    # def __str__(self):
    #     return "sin(cos(tan((x * {} + {})))) * sin(cos(tan((y * {} + {}))))".format(self.cx, self.dx, self.cy, self.dy)


class Checkered2(Function):
    def eval(self, x, y, normalized=True):
        newX = ((100 * x) % 100) / 100
        newY = ((100 * x) % 100) / 100
        z = asin(newX) + asin(newY)
        if normalized:
            z = max(self.zmin, min(self.zmax, z))
            return map_to(z, self.zmin, self.zmax, -1, 1)
        return z

    # def __str__(self):
    #     return "asin((x * {} + {})) + asin((x * {} + {}))".format(self.cx, self.dx, self.cy, self.dy)


class Sum(Function):
    def eval(self, x, y, normalized=True):
        newX = x * self.cx + self.dx
        newY = y * self.cy + self.dy
        z = newX + newY
        if normalized:
            z = max(self.zmin, min(self.zmax, z))
            return map_to(z, self.zmin, self.zmax, -1, 1)
        return z

    # def __str__(self):
    #     return "(x * {} + {}) + (y * {} + {})".format(self.cx, self.dx, self.cy, self.dy)


class Product(Function):
    def eval(self, x, y, normalized=True):
        newX = x * self.cx + self.dx
        newY = y * self.cy + self.dy
        z = newX * newY
        if normalized:
            z = max(self.zmin, min(self.zmax, z))
            return map_to(z, self.zmin, self.zmax, -1, 1)
        return z

    # def __str__(self):
    #     return "(x * {} + {}) * (y * {} + {})".format(self.cx, self.dx, self.cy, self.dy)


class Mod(Function):
    def eval(self, x, y, normalized=True):
        newX = x * self.cx + self.dx
        newY = y * self.cy + self.dy
        z = newX % newY
        if normalized:
            z = max(self.zmin, min(self.zmax, z))
            return map_to(z, self.zmin, self.zmax, -1, 1)
        return z

    # def __str__(self):
    #     return "(x * {} + {}) % (y * {} + {})".format(self.cx, self.dx, self.cy, self.dy)


class Mod2(Function):
    def eval(self, x, y, normalized=True):
        newX = x * self.cx + self.dx
        newY = y * self.cy + self.dy
        z = newY % newX
        if normalized:
            z = max(self.zmin, min(self.zmax, z))
            return map_to(z, self.zmin, self.zmax, -1, 1)
        return z

    # def __str__(self):
    #     return "(y * {} + {}) % (x * {} + {})".format(self.cy, self.dy, self.cx, self.dx)


class Well(Function):
    def eval(self, x, y, normalized=True):
        newX = x * self.cx + self.dx
        z = 1 - 2 / (newX ** 2) ** 8
        if normalized:
            z = max(self.zmin, min(self.zmax, z))
            return map_to(z, self.zmin, self.zmax, -1, 1)
        return z

    # def __str__(self):
    #     return "1 - 2 / ((x * {} + {}) ** 2) ** 8".format(self.cx, self.dx)


class Well2(Function):
    def eval(self, x, y, normalized=True):
        newY = y * self.cy + self.dy
        z = 1 - 2 / (newY ** 2) ** 8
        if normalized:
            z = max(self.zmin, min(self.zmax, z))
            return map_to(z, self.zmin, self.zmax, -1, 1)
        return z

    # def __str__(self):
    #     return "1 - 2 / ((x * {} + {}) ** 2) ** 8".format(self.cy, self.dy)


class PolarR(Function):
    def eval(self, x, y, normalized=True):
        newX = x * self.cx + self.dx
        newY = y * self.cy + self.dy
        z = sqrt(newX ** 2 + newY ** 2)
        if normalized:
            z = max(self.zmin, min(self.zmax, z))
            return map_to(z, self.zmin, self.zmax, -1, 1)
        return z

    # def __str__(self):
    #     return "sqrt((x * {} + {}) ** 2 + (y * {} + {}) ** 2)".format(self.cx, self.dx, self.cy, self.dy)


class PolarTheta(Function):
    def eval(self, x, y, normalized=True):
        newX = x * self.cx + self.dx
        newY = y * self.cy + self.dy
        try:
            z = atan(newY / newX)
        except ValueError:
            if newX > 0:
                if newY > 0:
                    z = pi / 4
                else:
                    z = 7 * pi / 4
            else:
                if newY > 0:
                    z = 3 * pi / 4
                else:
                    z = 5 * pi / 4
        if normalized:
            z = max(self.zmin, min(self.zmax, z))
            return map_to(z, self.zmin, self.zmax, -1, 1)
        return z

    # def __str__(self):
    #     return "atan((y * {} + {}) / (x * {} + {}))".format(self.cy, self.dy, self.cx, self.dx)


class GammaLower(Function):
    def eval(self, x, y, normalized=True):
        newX = x * self.cx + self.dx
        newY = y * self.cy + self.dy
        z = special.gammainc(abs(newX * 10 + 1), abs(newY * 10))
        if normalized:
            z = max(self.zmin, min(self.zmax, z))
            return map_to(z, self.zmin, self.zmax, -1, 1)
        return z

    # def __str__(self):
    #     return "lowerGamma(abs((x * {} + {}) * 10 + 1), abs((y * {} + {}) * 10))".format(
    #         self.cx, self.dx, self.cy, self.dy
    #     )


class GammaUpper(Function):
    def eval(self, x, y, normalized=True):
        newX = x * self.cx + self.dx
        newY = y * self.cy + self.dy
        z = special.gammainc(abs(newX * 10 + 1), abs(newY * 10))
        if normalized:
            z = max(self.zmin, min(self.zmax, z))
            return map_to(z, self.zmin, self.zmax, -1, 1)
        return z

    # def __str__(self):
    #     return "upperGamma(abs((x * {} + {}) * 10 + 1), abs((y * {} + {}) * 10))".format(
    #         self.cx, self.dx, self.cy, self.dy
    #     )


class FunctionNode:
    def __init__(self, prob, depth=0, func=None):
        # self.func = choice([Ripple, Ripple2, Sinkhole, Sinkhole2, Pulse, Bendy, Checkered, Checkered2, Sum, Product,
        #                     Well, Well2, PolarR, PolarTheta, GammaLower, GammaLower, GammaUpper, GammaUpper, InverseX,
        #                     InverseY])()
        if func is None:
            self.func = choice([Ripple, Ripple2, Sinkhole, Sinkhole2, Pulse, Bendy, Checkered, Checkered2, Well, Well2,
                                PolarR, PolarTheta, GammaLower, GammaUpper])()
        else:
            self.func = func
        if depth >= 4 or random() > prob:
            self.left = X()
            self.left.depth = 0
        else:
            newProb = prob * prob
            self.left = FunctionNode(newProb, depth + 1)
        if depth >= 4 or random() > prob:
            self.right = Y()
            self.right.depth = 0
        else:
            newProb = prob * prob
            self.right = FunctionNode(newProb, depth + 1)
        self.depth = max(self.left.depth + 1, self.right.depth + 1)

    def eval(self, x, y):
        newX = self.left.eval(x, y)
        newY = self.right.eval(x, y)
        return self.func.eval(newX, newY)


def createTree(root):
    tree = [str(root.func)]
    queue = [root.left, root.right]

    def checkQueue(q):
        tally = 0
        for x in q:
            if x is None:
                tally += 1
        return tally != len(q)

    while checkQueue(queue):
        curNode = queue.pop(0)
        if curNode is None:
            queue.append(None)
            queue.append(None)
            tree.append("#")
        elif type(curNode) in [X, Y]:
            queue.append(None)
            queue.append(None)
            tree.append(str(curNode))
        else:
            queue.append(curNode.left)
            queue.append(curNode.right)
            tree.append(str(curNode.func))

    return tree, ceil(log(len(tree), 2))


def _printTree(tree, depth):
    s = ""
    for i in range(depth):
        numCom1 = 2 ** ((depth - 1) - i) - 1
        numCom2 = 2 ** (depth - i)
        numCom3 = numCom1 + 1
        s += ',' * numCom1
        for x in range(2 ** i):
            if len(tree) > 0:
                nodeVal = tree.pop(0)
                if nodeVal != '#':
                    s += nodeVal
            s += ',' * numCom2
        s += ',' * numCom3
        s += '\n'
    return s


def saveTree(root, filename):
    tree, depth = createTree(root)
    with open("tests/{}".format(filename), 'w') as f:
        print(_printTree(tree, depth), end='', file=f)


def map_to(value, old_min, old_max, new_min, new_max):
    old_range = old_max - old_min
    new_range = new_max - new_min
    return new_min + new_range * (value - old_min) / old_range


if __name__ == '__main__':
    root = FunctionNode(1)
    print(root.depth)
    saveTree(root, 'test.csv')
    # Functions to add:
    #   Pascal's Triangle with mods
    #   Newton's method fractal (0)

