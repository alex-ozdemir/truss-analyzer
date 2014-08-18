# Alex Ozdemir
# aozdemir@hmc.edu
# 12 August 2014

# This file contains the application (GUI) layer of the Truss Analyzer
from Tkinter import *
from truss import *
from Vector import Vector
from LabelledWidgets import *

NODE_RADIUS = 7
NODE_SELECT_RADIUS = 10
LEFT_MOUSE = "<Button-1>"

STATE_ADD_NODE = 1
STATE_SELECT_NODE = 2

class TrussApp(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.pack()
        self.setupWindow()
        self.createWidgets()
        self.arrangeWidgets()

    def setupWindow(self):
        self.master.title("Truss Analyer")
        self.master.geometry("1000x600")

    def createWidgets(self):
        self.createTrussDisplay()
        self.controls = TrussControls(self, self.display)
        self.display.controls = self.controls

    def createTrussDisplay(self):
        self.display = TrussDisplay(self)
        
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
        self.nodeEdit = NodeEdit(self, self.display)
    def createAddNodeButton(self):
        self.addNode = Button(self, text="Add Node")
        self.addNode.state = STATE_ADD_NODE
        self.addNode.bind(LEFT_MOUSE, self.setState)
    def createSelectNodeButton(self):
        self.selectNode = Button(self, text="Select Node")
        self.selectNode.state = STATE_SELECT_NODE
        self.selectNode.bind(LEFT_MOUSE, self.setState)
    def setNodeDisplay(self, node):
        self.nodeEdit.displayNode(node)
    def arrangeWidgets(self):
        self.addNode.pack({"side": "top"})
        self.selectNode.pack({"side": "top"})
        self.nodeEdit.pack(side = TOP)
    def setState(self, event):
        self.display.state = event.widget.state
        print self.display.state
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
        self.update = Button(self, text = "Update", command=self.updateNode)
        self.remove = Button(self, text = "Remove", command=self.deleteNode)
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
    def deleteNode(self):
        self.display.deleteNode(self.node.position)
        
class TrussDisplay(Truss, Canvas):
    def __init__(self, master = None, nodes = [], members = []):
        self.trussclass = Truss
        Canvas.__init__(self, master)
        self.trussclass.__init__(self, [], [])
        self.setupGeometry()
        self.setupListeners()
    def setupGeometry(self):
        self['width'] = 700
        self['height'] = 580
        self['bd'] = 1
        self['bg'] = "#DDDDE4"
    def setupListeners(self):
        self.state = STATE_ADD_NODE
        self.bind(LEFT_MOUSE, self.click)
    def createNodes(self, nodes):
        for node in nodes:
            self.createNode(node)
    def getHeight(self):
        return self.winfo_height()
    def getWidth(self):
        return self.winfo_width()
    def click(self, event):
        if self.state == STATE_ADD_NODE:
            self.createNode(Vector((event.x, event.y)))
        elif self.state == STATE_SELECT_NODE:
            node = self.getNodeNear(Vector((event.x, event.y)), NODE_SELECT_RADIUS)
            if node != None:
                self.controls.setNodeDisplay(node)
        else:
            print "Error - click not handled properly"
    def createNode(self, position):
        try:
            self.trussclass.createNode(self, position)
            self.refresh(self.getNodeAt(position))
            print self
        except:
            print "error"
    def refresh(self, node):
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
    def deleteNode(self, position):
        node = self.getNodeNear(position, NODE_SELECT_RADIUS)
        if node != None:
            self.trussclass.deleteNode(self, node)
            self.delete(node.UIElement)
        else:
            print "No Node"
    
root = Tk()
app = TrussApp(root)
app.mainloop()
root.destroy()
