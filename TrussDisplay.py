# Alex Ozdemir
# aozdemir@hmc.edu
# 28 August 2014

# Contains the Truss Display for the truss analyzer

from Tkinter import *
from truss import *
from States import *

NODE_RADIUS = 7
NODE_SELECT_RADIUS = 10
LEFT_MOUSE = "<Button-1>"


class TrussDisplay(Truss, Canvas):
    def __init__(self, master = None, nodes = [], members = []):
        self.trussclass = Truss
        Canvas.__init__(self, master)
        self.trussclass.__init__(self, [], [])
        self.populate(nodes, members)
        self.setupGeometry()
        self.setupListeners()
    def populate(self, nodes, members):
        self.selectedNode = None
        self.createNodes(nodes)
        self.createMembers(members)
    def createNodes(self, nodes):
        for node in nodes:
            self.createNode(node)
    def createMembers(self, members):
        for member in members:
            node1 = self.getNodeAt(member.node1.position)
            node2 = self.getNodeAt(member.node2.position)
            self.connectNodes(node1, node2)
    def setupGeometry(self):
        self['width'] = 700
        self['height'] = 580
        self['bd'] = 1
        self['bg'] = "#DDDDE4"
    def setupListeners(self):
        self.state = STATE_ADD_NODE
        self.bind(LEFT_MOUSE, self.click)
    def getHeight(self):
        return self.winfo_height()
    def getWidth(self):
        return self.winfo_width()
    def selectNode(self, node):
        if self.selectedNode:
            self.itemconfig(self.selectedNode.UIElement, fill = "black")
            self.selectedNode = None
        if node:
            self.itemconfig(node.UIElement, fill = "blue")
            self.selectedNode = node  
            self.controls.setNodeDisplay(node)          
    def click(self, event):
        if self.state == STATE_ADD_NODE:
            self.createNode(Vector((event.x, event.y)))
            node = self.getNodeAt(Vector((event.x, event.y)))
            if node:
                self.selectNode(node)
        elif self.state == STATE_SELECT_NODE:
            node = self.getNodeNear(Vector((event.x, event.y)), NODE_SELECT_RADIUS)
            if node:
                self.selectNode(node)
        elif self.state == STATE_ADD_MEMBER:
            node = self.getNodeNear(Vector((event.x, event.y)), NODE_SELECT_RADIUS)
            if node:
                self.tempNode = node
                self.state = STATE_COMPLETE_MEMBER
                self.selectNode(node)
        elif self.state == STATE_COMPLETE_MEMBER:
            node = self.getNodeNear(Vector((event.x, event.y)), NODE_SELECT_RADIUS)
            if node:
                self.connectNodes(self.tempNode, node)
                self.state = STATE_ADD_MEMBER
                self.selectNode(None)
        else:
            print "Error - click not handled properly"
        print self
    def connectNodes(self, node1, node2):
        try:
            self.trussclass.connectNodes(self, node1, node2)
        except:
            print "Could not create member"
        self.refresh(self.getMemberWithNodes(node1, node2))
    def createNode(self, position):
        try:
            if type(position) == Node:
                self.addNode(position)
                position = position.position
            else:
                self.trussclass.createNode(self, position)
            self.refresh(self.getNodeAt(position))
        except:
            print "error creating node"
    def refreshMembers(self):
        for member in self.members:
            self.refresh(member)
    def refresh(self, item):
            if(type(item) == Node):
                node = item
                try:
                    self.delete(node.UIElement)
                except:
                    pass
                position = node.position
                node.UIElement = \
                    self.create_oval(position[0] - NODE_RADIUS, \
                                     position[1] - NODE_RADIUS, \
                                     position[0] + NODE_RADIUS, \
                                     position[1] + NODE_RADIUS, \
                                     fill = "black")
                for member in self.getMembersWithNode(node):
                    self.refresh(member)
            elif(type(item) == Member):
                member = item
                try:
                    self.delete(member.line)
                    self.delete(member.forceLabel)
                except:
                    pass
                p1 = member.node1.position
                p2 = member.node2.position
                member.line = self.create_line(p1[0], p1[1], p2[0], p2[1])
                if member.force != None:
                    member.forceLabel = self.create_text((p1[0] + p2[0]) / 2.0 + 10,
                                                         (p1[1] + p2[1]) / 2.0 + 10,
                                                         text = str(member.force))
    def removeAll(self):
        positions = [node.position for node in self.nodes]
        for position in positions:
            self.deleteNodeAt(position)
    def deleteNodeAt(self, position):
        node = self.getNodeAt(position)
        if node != None:
            super(TrussDisplay, self).deleteNode(node)
            self.delete(node.UIElement)
        else:
            print "No Node"
    def deleteMember(self, member):
        self.delete(member.line)
        try:
            self.delete(member.forceLabel)
        except:
            pass
        super(TrussDisplay, self).deleteMember(member)
    def loadFromStr(self, string):
        temp = eval(string)
        # TODO: PRINT STATEMENT
        print temp
        self.removeAll()
        self.populate(temp.nodes, temp.members)
        
    
