import pygame
import math



# Get the new x value of point pt (x, y) rotated about reference point
# refpt (x, y) by degrees clockwise
def rotatex(pt, refpt, deg):
    return (refpt[0] + (math.cos(math.radians(deg)) * (pt[0] - refpt[0])) + (math.sin(math.radians(deg)) * (pt[1] - refpt[1])))

# Get the new y value of point pt (x, y) rotated about reference point
# refpt (x, y) by degrees clockwise
def rotatey(pt, refpt, deg):
    return (refpt[1] + (-math.sin(math.radians(deg))*(pt[0] - refpt[0])) + (math.cos(math.radians(deg)) * (pt[1] - refpt[1])))

# Get the new point (x, y) rotated about the reference point refpt (x, y)
# by degrees clockwise
def rotatep(pt, refpt, deg):
    return (int(round(rotatex(pt, refpt, deg))), int(round(rotatey(pt, refpt, deg))))

#####################################################


class Shape:

    def __init__(self):
        self.id = None
        self.size = 1

    def set_points(self, x, y):
        self.points  = []
        self.corners = []
        self.sides   = []

    # num = referencing to which point of the piece 0 = central one
    # pt = what point on the Board
    def create(self, num, pt):
        self.set_points(0, 0)
        pm = self.points
        self.pts_map = pm
        x = pt[0] - self.pts_map[num][0]
        y = pt[1] - self.pts_map[num][1]
        self.set_points(x, y)


    # pt = goal point. Where will shape's points be after moving it to point pt
    def move_points(self, pt):
        x1 = self.points[0]
        x = pt[0] - x1[0]
        y = pt[1] - x1[1]
        array_points  = []
        array_corners = []
        array_sides   = []
        for p in self.points:
            array_points.append((p[0] + x, p[1] + y))
        self.points = array_points

        for c in self.corners:
            array_corners.append((c[0] + x, c[1] + y))
        self.corners = array_corners

        for s in self.sides:
            array_sides.append((s[0] + x, s[1] + y))
        self.sides = array_sides

    # Returns the points that would be covered by a
    # shape that is rotated 0, 90, 180, of 270 degrees
    # in a clockwise direction.
    def rotate(self, deg):
        self.points = [rotatep(pt, self.points[0], deg) for pt in self.points]
        self.corners = [rotatep(pt, self.points[0], deg) for pt in self.corners]
        self.sides = [rotatep(pt, self.points[0], deg) for pt in self.sides]

    # Returns the points that would be covered if the shape was flipped horizontally.
    def flip(self):
        # flip horizontally
        central_pt = self.points[0]
        def flip_h(point):
            x = 2*central_pt[0] - point[0]
            y = point[1]
            return (x, y)
        # flip the piece horizontally
        self.points = [flip_h(pt) for pt in self.points]
        self.corners = [flip_h(pt) for pt in self.corners]
        self.sides = [flip_h(pt) for pt in self.sides]

###############################

# All shape objects (pieces)
class I1(Shape):
    def __init__(self):
        self.id      = 'I1'
        self.size    = 1
    def set_points(self, x, y):
        self.points  = [(x, y)]
        self.corners = [(x + 1, y + 1), (x - 1, y - 1), (x + 1, y - 1), (x - 1, y + 1)]
        self.sides   = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]

class I2(Shape):
    def __init__(self):
        self.id      = 'I2'
        self.size    = 2
    def set_points(self, x, y):
        self.points  = [(x, y), (x, y + 1)]
        self.corners = [(x + 1, y - 1), (x - 1, y - 1), (x + 1, y + 2), (x - 1, y + 2)]
        self.sides   = [(x + 1, y), (x + 1, y + 1), (x, y + 2), (x - 1, y), (x - 1, y + 1), (x, y - 1)]

class I3(Shape):
    def __init__(self):
        self.id      = 'I3'
        self.size    = 3
    def set_points(self, x, y):
        self.points  = [(x, y), (x, y + 1), (x, y - 1)]
        self.corners = [(x + 1, y + 2), (x + 1, y - 2), (x - 1, y + 2), (x - 1, y - 2)]
        self.sides   = [(x + 1, y), (x + 1, y + 1), (x + 1, y - 1), (x, y + 2), (x - 1, y), (x - 1, y + 1), (x - 1, y - 1), (x, y - 2)]

class I4(Shape):
    def __init__(self):
        self.id      = 'I4'
        self.size    = 4
    def set_points(self, x, y):
        self.points  = [(x, y), (x, y + 1), (x, y + 2), (x, y - 1)]
        self.corners = [(x + 1, y - 2), (x - 1, y - 2), (x + 1, y + 3), (x - 1, y + 3)]
        self.sides   = [(x + 1, y), (x + 1, y + 1), (x + 1, y + 2), (x + 1, y - 1), (x, y + 3), (x - 1, y), (x - 1, y + 1), (x - 1, y + 2), (x - 1, y - 1), (x, y - 2)]

class I5(Shape):
    def __init__(self):
        self.id      = 'I5'
        self.size    = 5
    def set_points(self, x, y):
        self.points  = [(x, y), (x, y + 1), (x, y + 2), (x, y - 1), (x, y - 2)]
        self.corners = [(x + 1, y - 3), (x - 1, y - 3), (x + 1, y + 3), (x - 1, y + 3)]
        self.sides   = [(x + 1, y), (x + 1, y + 1), (x + 1, y + 2), (x + 1, y - 1), (x + 1, y - 2),(x, y + 3), (x - 1, y), (x - 1, y + 1), (x - 1, y + 2), (x - 1, y - 1), (x - 1, y - 2), (x, y - 3)]

class V3(Shape):
    def __init__(self):
        self.id      = 'V3'
        self.size    = 3
    def set_points(self, x, y):
        self.points  = [(x, y), (x, y + 1), (x + 1, y)]
        self.corners = [(x - 1, y - 1), (x + 2, y - 1), (x + 2, y + 1), (x + 1, y + 2), (x - 1, y + 2)]
        self.sides   = [(x + 1, y + 1), (x + 2, y), (x + 1, y - 1), (x, y - 1), (x - 1, y), (x - 1, y + 1), (x, y + 2)]

class L4(Shape):
    def __init__(self):
        self.id      = 'L4'
        self.size    = 4
    def set_points(self, x, y):
        self.points  = [(x, y), (x, y + 1), (x, y + 2), (x + 1, y)]
        self.corners = [(x - 1, y - 1), (x + 2, y - 1), (x + 2, y + 1), (x + 1, y + 3), (x - 1, y + 3)]
        self.sides   = [(x - 1, y), (x - 1, y + 1), (x - 1, y + 2), (x, y + 3), (x + 1, y + 2), (x + 1, y + 1), (x + 2, y), (x + 1, y - 1), (x, y - 1)]

class Z4(Shape):
    def __init__(self):
        self.id      = 'Z4'
        self.size    = 4
    def set_points(self, x, y):
        self.points  = [(x, y), (x, y + 1), (x + 1, y + 1), (x - 1, y)]
        self.corners = [(x - 2, y - 1), (x + 1, y - 1), (x + 2, y), (x + 2, y + 2), (x - 1, y + 2), (x - 2, y + 1)]
        self.sides   = [(x, y - 1), (x - 1, y - 1), (x - 2, y), (x - 1, y + 1), (x, y + 2), (x + 1, y + 2), (x + 2, y + 1), (x + 1, y)]

class O4(Shape):
    def __init__(self):
        self.id      = 'O4'
        self.size    = 4
    def set_points(self, x, y):
        self.points  = [(x, y), (x, y + 1), (x + 1, y + 1), (x + 1, y)]
        self.corners = [(x - 1, y - 1), (x + 2, y - 1), (x + 2, y + 2), (x - 1, y + 2)]
        self.sides   = [(x - 1, y), (x - 1, y + 1), (x, y + 2), (x + 1, y + 2), (x + 2, y + 1), (x + 2, y), (x + 1, y - 1), (x, y - 1)]

class L5(Shape):
    def __init__(self):
        self.id      = 'L5'
        self.size    = 5
    def set_points(self, x, y):
        self.points  = [(x, y), (x + 1, y), (x + 2, y), (x - 1, y), (x - 1, y + 1)]
        self.corners = [(x - 2, y - 1), (x + 3, y - 1), (x + 3, y + 1), (x, y + 2), (x - 2, y + 2)]
        self.sides   = [(x, y + 1), (x + 1, y + 1), (x + 2, y + 1), (x + 3, y), (x + 2, y - 1), (x + 1, y - 1), (x, y - 1), (x - 1, y - 1), (x - 2, y), (x - 2, y + 1), (x - 1, y + 2)]

class T5(Shape):
    def __init__(self):
        self.id      = 'T5'
        self.size    = 5
    def set_points(self, x, y):
        self.points  = [(x, y), (x, y + 1), (x, y + 2), (x - 1, y), (x + 1, y)]
        self.corners = [(x + 2, y - 1), (x + 2, y + 1), (x + 1, y + 3), (x - 1, y + 3), (x - 2, y + 1), (x - 2, y - 1)]
        self.sides   = [(x - 2, y), (x - 1, y + 1), (x - 1, y + 2), (x, y + 3), (x + 1, y + 2), (x + 1, y + 1), (x + 2, y), (x + 1, y - 1), (x, y - 1), (x - 1, y - 1)]

class V5(Shape):
    def __init__(self):
        self.id      = 'V5'
        self.size    = 5
    def set_points(self, x, y):
        self.points  = [(x, y), (x, y + 1), (x, y + 2), (x + 1, y), (x + 2, y)]
        self.corners = [(x - 1, y - 1), (x + 3, y - 1), (x + 3, y + 1), (x + 1, y + 3), (x - 1, y + 3)]
        self.sides   = [(x - 1, y), (x - 1, y + 1), (x - 1, y + 2), (x, y + 3), (x + 1, y + 2), (x + 1, y + 1), (x + 2, y + 1), (x + 3, y), (x + 2, y - 1), (x + 1, y - 1), (x, y - 1)]

class N(Shape):
    def __init__(self):
        self.id      = 'N'
        self.size    = 5
    def set_points(self, x, y):
        self.points  = [(x, y), (x + 1, y), (x + 2, y), (x, y - 1), (x - 1, y - 1)]
        self.corners = [(x + 1, y - 2), (x + 3, y - 1), (x + 3, y + 1), (x - 1, y + 1), (x - 2, y), (x - 2, y - 2)]
        self.sides   = [(x - 1, y), (x, y + 1), (x + 1, y + 1), (x + 2, y + 1), (x + 3, y), (x + 2, y - 1), (x + 1, y - 1), (x, y - 2), (x - 1, y - 2), (x - 2, y - 1)]

class Z5(Shape):
    def __init__(self):
        self.id      = 'Z5'
        self.size    = 5
    def set_points(self, x, y):
        self.points  = [(x, y), (x + 1, y), (x + 1, y + 1), (x - 1, y), (x - 1, y - 1)]
        self.corners = [(x + 2, y - 1), (x + 2, y + 2), (x, y + 2), (x - 2, y + 1), (x - 2, y - 2), (x, y - 2)]
        self.sides   = [(x - 2, y - 1), (x - 2, y), (x - 1, y + 1), (x, y + 1), (x + 1, y + 2), (x + 2, y + 1), (x + 2, y), (x + 1, y - 1), (x, y - 1), (x - 1, y - 2)]

class T4(Shape):
    def __init__(self):
        self.id      = 'T4'
        self.size    = 4
    def set_points(self, x, y):
        self.points  = [(x, y), (x, y + 1), (x + 1, y), (x - 1, y)]
        self.corners = [(x + 2, y - 1), (x + 2, y + 1), (x + 1, y + 2), (x - 1, y + 2), (x - 2, y + 1), (x - 2, y - 1)]
        self.sides   = [(x - 2, y), (x - 1, y + 1), (x, y + 2), (x + 1, y + 1), (x + 2, y), (x + 1, y - 1), (x, y - 1), (x - 1, y - 1)]

class P(Shape):
    def __init__(self):
        self.id      = 'P'
        self.size    = 5
    def set_points(self, x, y):
        self.points  = [(x, y), (x + 1, y), (x + 1, y - 1), (x, y - 1), (x, y - 2)]
        self.corners = [(x + 1, y - 3), (x + 2, y - 2), (x + 2, y + 1), (x - 1, y + 1), (x - 1, y - 3)]
        self.sides   = [(x, y + 1), (x + 1, y + 1), (x + 2, y), (x + 2, y - 1), (x + 1, y - 2), (x, y - 3), (x - 1, y - 2), (x - 1, y - 1), (x - 1, y)]

class W(Shape):
    def __init__(self):
        self.id      = 'W'
        self.size    = 5
    def set_points(self, x, y):
        self.points  = [(x, y), (x, y + 1), (x + 1, y + 1), (x - 1, y), (x - 1, y - 1)]
        self.corners = [(x + 1, y - 1), (x + 2, y), (x + 2, y + 2), (x - 1, y + 2), (x - 2, y + 1), (x - 2, y - 2), (x, y - 2)]
        self.sides   = [(x, y - 1), (x - 1, y - 2), (x - 2, y - 1), (x - 2, y), (x - 1, y + 1), (x, y + 2), (x + 1, y + 2), (x + 2, y + 1), (x + 1, y)]

class U(Shape):
    def __init__(self):
        self.id      = 'U'
        self.size    = 5
    def set_points(self, x, y):
        self.points  = [(x, y), (x, y + 1), (x + 1, y + 1), (x, y - 1), (x + 1, y - 1)]
        self.corners = [(x + 2, y - 2), (x + 2, y), (x + 2, y + 2), (x - 1, y + 2), (x - 1, y - 2)]
        self.sides   = [(x - 1, y - 1), (x - 1, y), (x - 1, y + 1), (x, y + 2), (x + 1, y + 2), (x + 2, y + 1), (x + 1, y), (x + 2, y - 1), (x + 1, y - 2), (x, y - 2)]

class F(Shape):
    def __init__(self):
        self.id      = 'F'
        self.size    = 5
    def set_points(self, x, y):
        self.points  = [(x, y), (x, y + 1), (x + 1, y + 1), (x, y - 1), (x - 1, y)]
        self.corners = [(x + 1, y - 2), (x + 2, y), (x + 2, y + 2), (x - 1, y + 2), (x - 2, y + 1), (x - 2, y - 1), (x - 1, y - 2)]
        self.sides   = [(x, y - 2), (x - 1, y - 1), (x - 2, y), (x - 1, y + 1), (x, y + 2), (x + 1, y + 2), (x + 2, y + 1), (x + 1, y), (x + 1, y - 1)]

class X(Shape):
    def __init__(self):
        self.id      = 'X'
        self.size    = 5
    def set_points(self, x, y):
        self.points  = [(x, y), (x, y + 1), (x + 1, y), (x, y - 1), (x - 1, y)]
        self.corners = [(x + 1, y - 2), (x + 2, y - 1), (x + 2, y + 1), (x + 1, y + 2), (x - 1, y + 2), (x - 2, y + 1), (x - 2, y - 1), (x - 1, y - 2)]
        self.sides   = [(x - 1, y - 1), (x - 2, y), (x - 1, y + 1), (x, y + 2), (x + 1, y + 1), (x + 2, y), (x + 1, y - 1), (x, y - 2)]

class Y(Shape):
    def __init__(self):
        self.id      = 'Y'
        self.size    = 5
    def set_points(self, x, y):
        self.points  = [(x, y), (x, y + 1), (x + 1, y), (x + 2, y), (x - 1, y)]
        self.corners = [(x + 3, y - 1), (x + 3, y + 1), (x + 1, y + 2), (x - 1, y + 2), (x - 2, y + 1), (x - 2, y - 1)]
        self.sides   = [(x - 2, y), (x - 1, y + 1), (x, y + 2), (x + 1, y + 1), (x + 2, y + 1), (x + 3, y), (x + 2, y - 1), (x + 1, y - 1), (x, y - 1), (x - 1, y - 1)]
