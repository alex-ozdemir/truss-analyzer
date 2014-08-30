# Alex Ozdemir
# aozdemir@hmc.edu
# 28 August 2014

# Contains the Edit tools for the truss analyzer

from Tkinter import *
from LabelledWidgets import *
from States import *

class TrussControls(Frame):
    def __init__(self, master, display):
        Frame.__init__(self, master)
        self.display = display
        self.grid()
        self.createWidgets()
        self.arrangeWidgets()
    def createWidgets(self):
        self.createAddNodeButton()
        self.createSelectNodeButton()
        self.createAddMemberButton()
        self.createSelectMemberButton()
        self.createComputeButton()
        self.nodeEdit = NodeEdit(self, self.display)
        self.memberEdit = MemberEdit(self, self.display)
        self.selectedButton = None
    def createAddNodeButton(self):
        self.addNode = Button(self, text="Add Node", command = self.onAddNodeClicked)
    def createSelectNodeButton(self):
        self.selectNode = Button(self, text="Select Node", command = self.onSelectNodeClicked)
    def createAddMemberButton(self):
        self.addMember = Button(self, text="Add Member", command = self.onAddMemberClicked)
    def createSelectMemberButton(self):
        self.selectMember = Button(self, text="Select Member", command = self.onSelectMemberClicked)
    def createComputeButton(self):
        self.compute = Button(self, text="Compute", command= self.compute)
    def onAddNodeClicked(self):
        self.setState(STATE_ADD_NODE)
        self.selectButton(self.addNode)
    def onSelectNodeClicked(self):
        self.setState(STATE_SELECT_NODE)
        self.selectButton(self.selectNode)
    def onAddMemberClicked(self):
        self.setState(STATE_ADD_MEMBER)
        self.selectButton(self.addMember)
    def onSelectMemberClicked(self):
        self.setState(STATE_SELECT_MEMBER)
        self.selectButton(self.selectMember)
    def arrangeWidgets(self):
        self.addNode.grid(row = 0, column = 0)
        self.selectNode.grid(row = 0, column = 1)
        self.addMember.grid(row = 1, column = 0)
        self.selectMember.grid(row = 1, column = 1)
        self.compute.grid(row = 2, column = 0, columnspan = 2)
        self.showNodeEdit()
        self.hideNodeEdit()
        self.showMemberEdit()
        self.hideMemberEdit()
    def setNodeDisplay(self, node):
        self.nodeEdit.displayNode(node)
    def setMemberDisplay(self, member):
        self.showMemberEdit()
        self.memberEdit.member = member
    def compute(self):
        self.display.computeForces()
        self.display.refreshMembers()
    def selectButton(self, button):
        if button:
            button.config(relief = SUNKEN)
        if self.selectedButton:
            self.selectedButton.config(relief = RAISED)
        self.selectedButton = button
    def setState(self, state):
        self.display.state = state
        if state in [STATE_SELECT_NODE, STATE_ADD_NODE]:
            self.showNodeEdit()
        else:
            self.hideNodeEdit()
            self.display.selectNode(None)
    def showNodeEdit(self):
        self.nodeEdit.grid(row = 3, column = 0, columnspan = 2, ipadx = 5, ipady = 5)
        self.hideMemberEdit()
    def hideNodeEdit(self):
        self.nodeEdit.grid_remove()
    def showMemberEdit(self):
        self.memberEdit.grid(row = 4, column = 0, columnspan = 2, ipadx = 5, ipady = 5)
        self.hideNodeEdit()
    def hideMemberEdit(self):
        self.memberEdit.grid_remove()
        
class NodeEdit(Frame):
    def __init__(self, master, display):
        Frame.__init__(self, master)
        self.node = None
        self.display = display
        self.grid()
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
        self.load = LabelEntry(self, "Load: ", 20)
        self.update = Button(self, text = "Update", command = self.updateNode)
        self.remove = Button(self, text = "Remove", command = self.deleteNode)
    def arrangeWidgets(self):
        self.label.grid(row = 0, column = 0, columnspan = 2)
        self.positionX.grid(row = 1, column = 0)
        self.positionY.grid(row = 1, column = 1)
        self.fixedX.grid(row = 2, column = 0)
        self.fixedY.grid(row = 2, column = 1)
        self.load.grid(row = 3, column = 0, columnspan = 2)
        self.update.grid(row = 4, column = 0)
        self.remove.grid(row = 4, column = 1)
    def displayNode(self, node):
        if self.node != node:
            self.node = node
            self.updateDisplay()
    def updateDisplay(self):
        if self.node:
            self.positionX.set(self.node.position[0])
            self.positionY.set(self.node.position[1])
            self.fixedY.set(self.node.fixedY)
            self.fixedX.set(self.node.fixedX)
            self.load.set(repr(self.node.loads))
        else:
            self.positionX.set("")
            self.positionY.set("")
            self.fixedX.set(False)
            self.fixedY.set(False)
            self.load.set("[]")
    def updateNode(self):
        if self.node:
            self.node.position = Vector((int(self.positionX.get()), int(self.positionY.get())))
            self.node.fixedX = 1 == self.fixedX.get()
            self.node.fixedY = 1 == self.fixedY.get()
            self.node.loads[:] = eval(self.load.get())
            self.display.refresh(self.node)
            self.display.selectNode(self.node)
    def deleteNode(self):
        self.display.deleteNodeAt(self.node.position)


class MemberEdit(Frame):
    def __init__(self, master, display):
        Frame.__init__(self, master)
        self.member = None
        self.display = display
        self.grid()
        self.config(relief = GROOVE, bd = 2)
        self.createWidgets()
        self.arrangeWidgets()
    def createWidgets(self):
        self.label = Label(self, text = "Member")
        self.remove = Button(self, text = "Remove", command = self.deleteMember)
    def arrangeWidgets(self):
        self.label.grid(row = 0, column = 0)
        self.remove.grid(row = 1, column = 0)
    def deleteMember(self):
        self.display.deleteMember(self.member)