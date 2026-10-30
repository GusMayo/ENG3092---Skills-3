import matplotlib.pyplot as plt
import numpy as np
from abc import ABCMeta, abstractmethod

#create point class:
class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self):
        plt.scatter(self.x, self.y)

#create abstract shape class (copied from brief):
class Shape(metaclass = ABCMeta):
    def __init__(self):
        pass

    @abstractmethod
    def draw(self):
        pass

#create a shape child class for polygons
class Polygon(Shape):
    def __init__(self, point_list):
        self.point_list = point_list

    def draw(self):
        #create arrays for the x and y coordinates of each point in the point list and plot them:
        xs = [point.x for point in self.point_list]
        ys = [point.y for point in self.point_list]

        xs.append(xs[0])
        ys.append(ys[0])

        plt.plot(xs, ys)

#create a polygon child class for rectangle
class Rectangle(Polygon):
    def __init__(self, corner, w, h, theta):
        self.corner = corner
        self.w = w
        self.h = h
        self.theta = theta

        #create a points list for the rectangular polygon:
        x1 = self.corner.x
        y1 = self.corner.y #first point is the corner inputted by the user

        x2 = self.corner.x + self.h * np.sin(self.theta)
        y2 = self.corner.y + self.h * np.cos(self.theta) #find second point using trig

        x3 = x2 + self.w * np.cos(self.theta)
        y3 = y2 - self.w * np.sin(self.theta) #find third point using trig

        x4 = self.corner.x + self.w * np.cos(self.theta)
        y4 = self.corner.y - self.w * np.sin(self.theta) #find 4th point using trig

        xs = [x1, x2, x3, x4]
        ys = [y1, y2, y3, y4]

        point_list = [Point(xs[i], ys[i]) for i in range(len(xs))] #point list has been created

        Polygon.__init__(self, point_list)#initiate a polygon with the 4 corners found as the points list

#create a rectangle child class for square:
class Square(Rectangle):
    def __init__(self, corner, a, theta):
        #call the __init__ function for rectangle, but both w and h are equal to a
        Rectangle.__init__(self, corner, a, a, theta)

#create a shape child class for Ellipse:
class Ellipse(Shape):
    def __init__(self, center, a, b, theta):
        self.center = center
        self.a = a
        self.b = b
        self.theta = theta

    def draw(self):
        #draw ellipse using parametric equation:
        phis = np.linspace(-np.pi, np.pi, 100)

        xs = np.array([self.center.x + (self.a * np.cos(phis[i]) * np.cos(self.theta) - self.b * np.sin(phis[i]) * np.sin(self.theta)) for i in range(phis.shape[0])])
        ys = np.array([self.center.y + (self.a * np.cos(phis[i]) * np.sin(self.theta) + self.b * np.sin(phis[i]) * np.cos(self.theta)) for i in range(phis.shape[0])])

        plt.plot(xs, ys)

#create an Ellipse child class for circle:
class Circle(Ellipse):
    def __init__(self, center, r):
        #initiate an Ellipse but with a = b = r. rotation fixed at 0 as it does not matter for a circle.
        Ellipse.__init__(self, center, r, r, 0)

plt.gca().set_aspect('equal', adjustable='box') #sets plt axes to the same scale to maintain shape scale

s = Square(Point(2, 2), 4, 0.3)#initiates shape

s.draw()
plt.show()
