# Alex Ozdemir
# aozdemir@hmc.edu
# 9 August 2014
from Vector import Vector
from Matrix import Matrix
from operator import add

# This file contains 3 Classes:
#  Truss - an engineering trus, composed of nodes and members
#  Node - a joint between members in a truss
#  Member - a connection between nodes in a truss

class Node(object):
    def __init__(self, position, loads = [], fixedX = False, fixedY = False):
        self.position = Vector(position)
        self.loads =[Vector(load) for load in loads]
        self.fixedX = fixedX
        self.fixedY = fixedY
    def __eq__(self, other):
        return self.position == other.position
    def __str__(self):
        result = "Node at " + str(self.position)
        if len(self.loads) > 0:
            result += ", with loads " + str(self.loads)
        if self.fixedX:
            result += ", with X fixed"
        if self.fixedY:
            result += ", with Y fixed"
        return result
    def __repr__(self):
        return "Node(" +\
               repr(self.position) + ", " + \
               repr(self.loads) + ", " + \
               repr(self.fixedX) + ", " + \
               repr(self.fixedY) + ")"

class Member(object):
    def __init__(self, node1, node2, force = None):
        self.node1 = node1
        self.node2 = node2
        self.force = force
    def hasNode(self, node):
        return node in [self.node1, self.node2]
    def getVector(self, node):
        if node == self.node1:
            return self.node1.position - self.node2.position
        elif node == self.node2:
            return self.node2.position - self.node1.position
        else: raise Exception("Cannot get vector for %s, because it is not it %s" \
               % (str(node), str(member)))
    def __eq__(self, other):
        return sameElements([self.node1, self.node2], [other.node1, other.node2]) and \
               self.force == other.force
    def __str__(self):
        res = "Member from %s to %s" % (str(self.node1.position), str(self.node2.position))
        if self.force != None:
            res += " with force %.2f" % (self.force)
        return res
    def __repr__(self):
        return "Member(" + \
               repr(self.node1) + ", " + \
               repr(self.node2) + ", " + \
               repr(self.force) + ")"

class Truss(object):
    def __init__(self, nodes = [], members = []):
        self.nodes = nodes
        self.members = members
    def createNode(self, position):
        self.addNode(Node(position))
    def addNode(self, node):
        if node in self.nodes:
            raise Exception("Tried to add the  " + str(node) + \
                            " to the truss \n" + str(self) + \
                            " but it was already there")
        else:
            self.nodes.append(node)
    def getNodeNear(self, position, radius):
        p = Vector(position)
        nearestNode = min([((n.position - p).length, n) for n in self.nodes])[1]
        if (nearestNode.position - p).length < radius:
            return nearestNode
        else:
            return None
    def deleteNode(self, node):
        for n in self.nodes:
            if node == n:
                self.nodes.remove(n)
                self.removeMembers(n)
                return
        raise Exception("The node %s does not exist in %s" % (str(node), str(self)))
    def removeMembers(self, node):
        self.members[:] = [member for member in self.members if not member.hasNode(node)]
    def connectNodes(self, node1, node2):
        newMember = Member(node1, node2)
        if newMember not in self.members:
            if node1 in self.nodes and node2 in self.nodes:
                self.members.append(newMember)
            else:
                 raise Exception("Tried to add the  " + str(newMember) + \
                                 " to the truss, but those nodes don't exist")
        else:
            raise Exception("Tried to add the  " + str(newMember) + \
                            " to the truss, but it was already there")
    def computeForces(self):
        self.getEquilibriumMatrix()
        self.solveMatrix()
        for c in range(self.matrix.width - 1):
            self.members[c].force = self.matrix[c][self.matrix.width - 1]
    def solveMatrix(self):
        if self.matrix.width > self.matrix.height + 1:
            raise Exception("The problem is under-defined")
        self.matrix.rref()
    def getEquilibriumMatrix(self):
        self.matrix = []
        for node in self.nodes:
            self.addXEquation(node)
            self.addYEquation(node)
        self.matrix = Matrix(self.matrix)
        return self.matrix

    def addXEquation(self, node):
        if not node.fixedX:
            row = []
            for member in self.members:
                if member.hasNode(node):
                    vector = member.getVector(node)
                    row.append(float(vector[0]) / vector.length)
                else:
                    row.append(0)
            row.append(-reduce(add,[x[0] for x in node.loads], 0))
            self.matrix.append(row)
    def addYEquation(self, node):
        if not node.fixedY:
            row = []
            for member in self.members:
                if member.hasNode(node):
                    vector = member.getVector(node)
                    row.append(float(vector[1]) / vector.length)
                else:
                    row.append(0)
            row.append(-reduce(add,[x[1] for x in node.loads], 0))
            self.matrix.append(row)
            
    def __eq__(self, other):
        return sameElements(self.nodes, other.nodes) and \
               sameElements(self.members, other.members)
    def __str__(self):
        return "Truss: \n" + self.nodeStr() + self.memberStr()
    def nodeStr(self):
        result = " Nodes: \n"
        for node in self.nodes:
            result += "   " + str(node) + ",\n"
        return result[:-2] + "\n"
    def memberStr(self):
        result = " Members: \n"
        for member in self.members:
            result += "   " + str(member) + ",\n"
        return result[:-2] + "\n"
    def __repr__(self):
        return "Truss(" + \
               repr(self.nodes) + ", " + \
               repr(self.members) + ")"

def sameElements(l1, l2):
    return all([e in l1 for e in l2]) and \
           all([e in l2 for e in l1])    
def test_init():
    a = Node((2, 3), [])
def test_str():
    a = Node((2, 3), [])
    print a
def test_eq():
    a = Node((4,5))
    b = Node((4,5))
    if a == b:
        print "test passed"
    else:
        print "test failed"
    c = Node((5,6))
    t1 = Truss([a,c])
    t2 = Truss([a])
    if t1 == t2:
        print "test failed"
    else:
        print "test passed"
def test_duplicate_connection():
    a = Node((4,5))
    b = Node((4,6))
    b.addConnection(a)
    try:
        b.addConnection(a)
        print "test failed"
    except:
        print "test passed"
def test_repr():
    t = Truss()
    t.createNode((4,5))
    print "Original: "
    print t
    print "Representation: "
    print repr(t)
    print "Recreated: "
    print eval(repr(t))
    if eval(repr(t)) == t:
        print "test passed"
    else:
        print "test failed"
def simpleTruss():
    t = Truss()
    t.createNode((0,0))
    t.createNode((3,3))
    t.createNode((6,0))
    t.connectNodes(Node((0,0)), Node((3,3)))
    t.connectNodes(Node((0,0)), Node((6,0)))
    t.connectNodes(Node((6,0)), Node((3,3)))
    t.nodes[1].loads.append(Vector((0,-100)))
    t.nodes[0].fixedX = True
    t.nodes[0].fixedY = True
    t.nodes[2].fixedY = True
    print "t:\n",t
    return t
t = simpleTruss()
