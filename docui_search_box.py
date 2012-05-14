from Tkinter import *
from ttk import *
import re

class DocSearchBox(Frame):
    def __init__(self, master, parent, document_obj=None):
         Frame.__init__(self, parent)
         self.master = master
         self.document_obj = document_obj
         self.initUI()

    def initUI(self):
         self.box = Text(self,state='disabled', width=80, height=20)
         self.box.grid(row=0, column=0, columnspan=10)
