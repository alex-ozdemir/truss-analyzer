# Alex Ozdemir
# aozdemir@hmc.edu
# 9 August 2014

# Vector class
from math import sqrt
from operator import add
from string import join

class Vector(tuple):
    def __init__(self, xs):
        self.superclass = tuple
        self.superclass.__init__(xs)
        self.size = self.superclass.__len__(self)
        self.length = sqrt(reduce(add, [x ** 2 for x in self], 0))
    def __len__(self):
        return self.length
    def __add__(self, other):
        return Vector([self[i] + other[i] for i in range(self.size)])
    def __sub__(self, other):
        return Vector([self[i] - other[i] for i in range(self.size)])
    def __neg__(self):
        return Vector([-self[i] for i in range(self.size)])
    def __repr__(self):
        return "Vector(%s)" % (self.superclass.__repr__(self))
    def __str__(self):
        return "<" + join([str(x) for x in self],", ") + ">"
