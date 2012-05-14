from Tkinter import *
from ttk import *
import re
#from docui_search_box import DocSearchBox
class DocSearchUI(Frame):
    def __init__(self, master, parent, document_obj=None, status=None):
         Frame.__init__(self, parent)
         self.status = status
         self.parent = parent
         self.master = master
         self.document_obj = document_obj
         self.initUI()

    def initUI(self):
         self.columnconfigure(5, weight=1)
         self.rowconfigure(2, weight=1)
         self.search_label = Label(self, text='Keyword:')
         self.search_label.grid(row=0, column=0, padx=5)

         self.keywords = StringVar()
         self.keywords.set('')
         self.search_bar = Entry(self, width=30,textvariable=self.keywords)
         self.search_bar.grid(row=0, column=1, columnspan=2, sticky=W+E)

         self.search_button = Button(self, text="Search", 
                              command=self.handler_search)
         self.search_button.grid(row=0, column=3, padx=5)

         self.pack(fill=BOTH, expand='yes')
         #self.pack(expand='y')

    def handler_search(self):
         if self.keywords.get() == '': 
             self.status.set('You cannot search for empty string.')
         else:
             contents = self.document_obj.text_content.get('1.0', END)
             results = [ss.start() for ss in re.finditer(self.keywords.get(), contents)]
             self.status.set('Found ' + str(len(results)) + ' matched keyword %s' % self.keywords.get())
         #self.result_windows_frame = Frame(self, relief=FLAT)
         #self.result_windows = Text(self.result_windows_frame, state='disabled')
         #self.result_windows.pack(side=LEFT, fill=BOTH, expand=1, sticky=W+E)
         #self.scroll = Scrollbar(self.result_windows_frame, orient=VERTICAL)
 

         


