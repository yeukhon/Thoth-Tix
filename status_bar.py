from Tkinter import *
from ttk import *

class StatusBar(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)
        self.status = StringVar()
        self.label = Label(self, relief=SUNKEN, anchor=W, textvariable=self.status,\
                           font=('arial', 16, 'normal'))
        self.status.set('Running..')
        self.label.pack(fill=X)
        self.pack()

    def set(self, format, *args):
        self.label.config(text=format % args)
        self.label.update_idletasks()

    def clear(self):
        self.label.config(text="")
        self.label.update_idletasks()
