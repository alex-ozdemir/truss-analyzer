# Alex Ozdemir
# aozdemir@hmc.edu
# 12 August 2014

# This file contains an implementation of a method which determines the Reduced Row Echelon
#  form of a matrix.

from string import join

def negligible(x):
    return abs(x) < 0.00001

class Matrix(object):
    def __init__(self, matrix):
        """Creates a matrix as a list of row/lists"""
        self.matrix = matrix
        self.setAndValidateDimensions()
        
    def setAndValidateDimensions(self):
        self.height = len(self.matrix)
        assert self.height > 0, "Error: Matrix must have a positive number of rows"
        self.width = len(self.matrix[0])
        assert self.width > 0, "Error: Matrix must have a positive number of columns"
        self.checkRowLengths()

    def checkRowLengths(self):
        for r in range(self.height - 1):
            assert len(self.matrix[r]) == len(self.matrix[r + 1]), \
                   "Error: Rows are not of the same length"
            
    def rref(self):
        self.toFloat()
        for c in range(self.width):
            self.makeNonZeroDiagonal(c)
            for r in range(self.height):
                self.normalizeCell(r, c)
    def toFloat(self):
        for r in range(self.height):
            for c in range(self.width):
                self.matrix[r][c] = float(self.matrix[r][c])
    def addMultipleOfRow(self, rToChange, rToAdd, multiple = 1):
        for c in range(self.width):
            self.matrix[rToChange][c] += multiple * self.matrix[rToAdd][c]
    def scaleRow(self, r, scale):
        for c in range(self.width):
            self.matrix[r][c] *= scale
    def makeNonZeroDiagonal(self, c):
        if  c < self.height and negligible(self.matrix[c][c]):
            self.addMultipleOfRow(c, self.findNonZeroRowNum(c))           
    def normalizeCell(self, r, c):
        if r == c:
            self.makeCell1(r, c)
        else:
            self.makeCell0(r, c)
    def makeCell1(self, r, c):
        if not negligible(self.matrix[r][c]):
            scale = 1.0 / self.matrix[r][c]
            self.scaleRow(r, scale)
        else:
            print self
            raise Exception("Zero Diagonal")
    def findNonZeroRowNum(self, c):
        for r_nonzero in range(c, self.height):
            if not negligible(self.matrix[r_nonzero][c]):
                return r_nonzero
        raise Exception("The was an all-zero column in the matrix")
    def makeCell0(self, r, c):
        if c < self.height:
            if not negligible(self.matrix[r][c]):
                scale = -self.matrix[r][c] / self.matrix[c][c]
                self.addMultipleOfRow(r, c, scale)
    def __getitem__(self, i):
        return self.matrix[i]
    def __iter__(self):
        return iter(self.matrix)
    def __str__(self):
        return join([str(row) for row in self.matrix], "\n")
