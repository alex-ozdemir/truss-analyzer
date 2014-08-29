# Alex Ozdemir
# aozdemir@hmc.edu
# 12 August 2014

# This file contains the application (GUI) layer of the Truss Analyzer
import tkFileDialog
from Tkinter import *
from Vector import Vector
from TrussControls import *
from TrussDisplay import *

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
        self.display.loadFromStr(string)
        
    def arrangeWidgets(self):
        self.display.pack(side = LEFT, fill = BOTH, expand = 1)
        self.controls.pack(side = RIGHT)

        
    
root = Tk()
app = TrussApp(root)
app.mainloop()
root.destroy()
