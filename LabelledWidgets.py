from Tkinter import *
class LabelEntry(Frame):
    def __init__(self, master, label, width = None):
        Frame.__init__(self, master)
        self.pack()
        self.content = StringVar()
        self.label = Label(self, text = label)
        self.entry = Entry(self, textvariable = self.content)
        if width:
            self.entry.config(width = width)
        self.label.pack(side=LEFT)
        self.entry.pack(side=LEFT)
    def set(self, text):
        self.content.set(text)
    def get(self):
        return self.content.get()

class LabelCheck(Frame):
    def __init__(self, master, label):
        Frame.__init__(self, master)
        self.pack()
        self.content = IntVar()
        self.label = Label(self, text = label)
        self.check = Checkbutton(self, variable = self.content)
        self.label.pack(side=LEFT)
        self.check.pack(side=LEFT)
    def set(self, value):
        self.content.set(value)
    def get(self):
        return self.content.get()


        
