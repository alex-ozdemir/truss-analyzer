# Alex Ozdemir
# aozdemir@hmc.edu
# 12 August 2014

# This file contains the application (GUI) layer of the Truss Analyzer
from Tkinter import *

class TrussApp(Frame):
    def __init__(self, master = None):
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

    def createTrussDisplay(self):
        self.TrussDisplay = Canvas(self, width = 800, height = 500)

    def arrangeWidgets(self):
        self.TrussDisplay.pack({"side": "left"})

root = Tk()
app = TrussApp(root)
app.mainloop()
root.destroy()
