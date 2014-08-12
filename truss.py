# Alex Ozdemir
# aozdemir@hmc.edu
# 9 August 2014

class Node(object):
    def __init__(self, position, loads = [], fixedX = False, fixedY = False):
        self.position = position
        self.loads = loads
        self.fixedX = fixedX
        self.fixedY = fixedY
    def __eq__(self, other):
        return self.position.__eq__(other.position)
    def __str__(self):
        return "Node at " + str(self.position) + ", connected to: " + str(self.members)

class Member(object):
    def __init__(self, node1, node2, stress = None):
        self.node1 = node1
        self.node2 = node2
        self.stress = stress
    def hasNode(self, node):
        return node in [self.node1, self.node2]
    def __eq__(self, other):
        return set(self.node1, self.node2) == set(other.node1, other.node2)
    

class Truss(object):
    def __init__(self):
        self.nodes = []
        self.members = []
    def createNode(self, position):
        self.addNode(Node(position))
    def addNode(self, node):
        if node in self.nodes:
            raise Exception("Tried to add the node " + str(node) + \
                            " to the truss " + str(self) + \
                            " but it was already there")
        else:
            self.nodes.append(node)
    def connectNodes(self, node1, node2):
        newMember = Member(node1, node2)
        if newMember not in self.members and\
           node1 in self.nodes and\
           node2 in self.nodes:
            self.members.append(newMember)
            
    def __eq__(self, other):
        return set(self.nodes) == set(other.nodes)
    def __str__(self):
        result = "Truss with nodes: \n"
        for node in self.nodes:
            result += str(node) + ",\n"
        return result[:-2]

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
    print repr(t)
    print eval(repr(t))
    if eval(repr(t)) == t:
        print "test passed"
    else:
        print "test failed"
