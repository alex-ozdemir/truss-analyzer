# Alex Ozdemir
# aozdemir@hmc.edu
# 12 August 2014

# This file contains the application (GUI) layer of the Truss Analyzer
import tkFileDialog
from Tkinter import *
from truss import *
from Vector import Vector
from LabelledWidgets import *

NODE_RADIUS = 7
NODE_SELECT_RADIUS = 10
LEFT_MOUSE = "<Button-1>"

STATE_ADD_NODE = 1
STATE_SELECT_NODE = 2
STATE_ADD_MEMBER = 3
STATE_COMPLETE_MEMBER = 4

class TrussApp(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.pack()
        self.setupWindow()
        self.createWidgets()
        self.createMenu()
        self.arrangeWidgets()

    def setupWindow(self):
        self.master.title("Truss Analyer")
        self.master.geometry("1000x600")
        self.setFileDialogOptions()

    def setFileDialogOptions(self):
        self.fileDialogOptions = options = {}
        options['defaultextension'] = '.truss'
        options['filetypes'] = [('truss files', '.truss'), ('all files', '.*')]
        options['initialdir'] = 'C:\\Users\\Alex'
        options['parent'] = root
        options['title'] = 'Select a Truss file to save or load'

    def createWidgets(self):
        self.display = TrussDisplay(self)
        self.controls = TrussControls(self, self.display)
        self.display.controls = self.controls

    def createMenu(self):
        self.menuBar = Menu(self.master)
        self.fileMenu = Menu(self.menuBar, tearoff = 0)
        self.fileMenu.add_command(label = "Save As", command = self.save)
        self.fileMenu.add_command(label = "Load", command = self.load)
        self.menuBar.add_cascade(label = "File", menu = self.fileMenu)
        self.master.config(menu = self.menuBar)        

    def save(self):
        fileName = tkFileDialog.asksaveasfilename(**self.fileDialogOptions)
        if fileName:
            f = open(fileName, 'w')
            f.write(repr(self.display))
            f.close()
    def load(self):
        f = tkFileDialog.askopenfile(mode='r', **self.fileDialogOptions)
        string = f.read()
        f.close()
        temp = eval(string)
        print temp
        self.display.removeAll()
        self.display.populate(temp.nodes, temp.members)
        
    def arrangeWidgets(self):
        self.display.pack({"side": "left"})
        self.controls.pack({"side": "right"})

class TrussControls(Frame):
    def __init__(self, master, display):
        Frame.__init__(self, master)
        self.display = display
        self.pack()
        self.createWidgets()
        self.arrangeWidgets()
    def createWidgets(self):
        self.createAddNodeButton()
        self.createSelectNodeButton()
        self.createAddMemberButton()
        self.createComputeButton()
        self.nodeEdit = NodeEdit(self, self.display)
    def createAddNodeButton(self):
        self.addNode = Button(self, text="Add Node", command= ( \
            lambda : self.setState(STATE_ADD_NODE)))
    def createSelectNodeButton(self):
        self.selectNode = Button(self, text="Select Node", command= ( \
            lambda : self.setState(STATE_SELECT_NODE)))
    def createAddMemberButton(self):
        self.addMember = Button(self, text="Add Member", command= ( \
            lambda : self.setState(STATE_ADD_MEMBER)))
    def createComputeButton(self):
        self.compute = Button(self, text="Compute", command= self.compute)
    def setNodeDisplay(self, node):
        self.nodeEdit.displayNode(node)
    def arrangeWidgets(self):
        self.addNode.pack(side = TOP)
        self.selectNode.pack(side = TOP)
        self.addMember.pack(side = TOP)
        self.compute.pack(side = TOP)
        self.nodeEdit.pack(side = TOP)
    def compute(self):
        self.display.computeForces()
        self.display.refreshMembers()
    def setState(self, state):
        self.display.state = state
class NodeEdit(Frame):
    def __init__(self, master, display):
        Frame.__init__(self, master)
        self.node = None
        self.display = display
        self.pack()
        self.setup()
        self.createWidgets()
        self.arrangeWidgets()
    def setup(self):
        self.config(relief = GROOVE, bd = 2)
    def createWidgets(self):
        self.label = Label(self, text = "Node")
        self.positionX = LabelEntry(self, "X Position: ", 3)
        self.positionY = LabelEntry(self, "Y Position: ", 3)
        self.fixedX = LabelCheck(self, "Fix X: ")
        self.fixedY = LabelCheck(self, "Fix Y: ")
        self.load = LabelEntry(self, "Load: ", 10)
        self.update = Button(self, text = "Update", command = self.updateNode)
        self.remove = Button(self, text = "Remove", command = self.deleteNode)
    def arrangeWidgets(self):
        self.label.pack(side = TOP)
        self.positionY.pack(side = TOP)
        self.positionX.pack(side = TOP)
        self.fixedY.pack(side = TOP)
        self.fixedX.pack(side = TOP)
        self.load.pack(side = TOP)
        self.update.pack(side = TOP)
        self.remove.pack(side = TOP)
    def displayNode(self, node):
        if self.node != node:
            self.node = node
            self.updateDisplay()
    def updateDisplay(self):
        self.positionX.set(self.node.position[0])
        self.positionY.set(self.node.position[1])
        self.fixedY.set(self.node.fixedY)
        self.fixedX.set(self.node.fixedX)
        self.load.set(repr(self.node.loads))
    def updateNode(self):
        self.node.position = Vector((int(self.positionX.get()), int(self.positionY.get())))
        self.node.fixedX = 1 == self.fixedX.get()
        self.node.fixedY = 1 == self.fixedY.get()
        self.node.loads[:] = eval(self.load.get())
        self.display.refresh(self.node)
        self.display.selectNode(self.node)
    def deleteNode(self):
        self.display.deleteNodeAt(self.node.position)
        
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
                self.selectNode(node)            
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
                if member.force:
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
    
root = Tk()
app = TrussApp(root)
app.mainloop()
root.destroy()
