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
        return self.position == other.position and \
               self.loads == other.loads and \
               self.fixedX == other.fixedX and \
               self.fixedY == other.fixedY
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
    def __init__(self, node1, node2, stress = None):
        self.node1 = node1
        self.node2 = node2
        self.stress = stress
    def hasNode(self, node):
        return node in [self.node1, self.node2]
    def __eq__(self, other):
        return set(self.node1, self.node2) == set(other.node1, other.node2) and \
               self.stress == other.stress
    def __str__(self):
        return "Member from " + str(self.node1.position) + " to " + \
               str(self.node2.position)
    def __repr__(self):
        return "Member(" + \
               repr(self.node1) + ", " + \
               repr(self.node2) + ", " + \
               repr(self.stress) + ")"

class Truss(object):
    def __init__(self, nodes = [], members = []):
        self.nodes = nodes
        self.members = members
    def createNode(self, position):
        self.addNode(Node(position))
    def addNode(self, node):
        if node in self.nodes:
            raise Exception("Tried to add the node " + str(node) + \
                            " to the truss \n" + str(self) + \
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
        return set(self.nodes) == set(other.nodes) and \
               set(self.members) == set(other.members)
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
