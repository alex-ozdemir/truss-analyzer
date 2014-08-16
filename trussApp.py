# Alex Ozdemir
# aozdemir@hmc.edu
# 12 August 2014

# This file contains the application (GUI) layer of the Truss Analyzer
from Tkinter import *
from truss import *
from Vector import Vector

NODE_RADIUS = 7
LEFT_MOUSE = "<Button-1>"

STATE_ADD_NODE = 1
STATE_DELETE_NODE = 2

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
        self.createDeleteNodeButton()
    def createAddNodeButton(self):
        self.addNode = Button(self, text="Add Node")
        self.addNode.state = STATE_ADD_NODE
        self.addNode.bind(LEFT_MOUSE, self.setState)
    def createDeleteNodeButton(self):
        self.deleteNode = Button(self, text="Delete Node")
        self.deleteNode.state = STATE_DELETE_NODE
        self.deleteNode.bind(LEFT_MOUSE, self.setState)
        
    def arrangeWidgets(self):
        self.addNode.pack({"side": "top"})
        self.deleteNode.pack({"side": "right"})
    def setState(self, event):
        self.display.state = event.widget.state
        print self.display.state
        print self.deleteNode

class TrussDisplay(Truss, Canvas):
    def __init__(self, master = None, nodes = [], members = []):
        self.trussclass = Truss
        Canvas.__init__(self, master)
        self.trussclass.__init__(self, nodes, members)
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
        
    def getHeight(self):
        return self.winfo_height()
    def getWidth(self):
        return self.winfo_width()
    def click(self, event):
        if self.state == STATE_ADD_NODE:
            self.createNode(Vector((event.x, event.y)))
        elif self.state == STATE_DELETE_NODE:
            self.deleteNode(Vector((event.x, event.y)))
        else:
            print "Error - click not handled properly"
    def createNode(self, position):
        try:
            self.trussclass.createNode(self, position)
            self.create_oval(position[0] - NODE_RADIUS, \
                             position[1] - NODE_RADIUS, \
                             position[0] + NODE_RADIUS, \
                             position[1] + NODE_RADIUS, \
                             fill = "black")
            print self
        except:
            print "error"
    def deleteNode(self, position):
        
    
root = Tk()
app = TrussApp(root)
app.mainloop()
root.destroy()
