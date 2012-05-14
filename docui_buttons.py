from Tkinter import *
from ttk import *
import tkMessageBox

class DocSideButtons(Frame):
    def __init__(self, parent, document_obj=None, user=None):
         Frame.__init__(self, parent)
         self.parent = parent
         self.user = user
         self.document_obj = document_obj
         self.docid = self.document_obj.document.info['id']
         self.initUI()

    def initUI(self):
         self.columnconfigure(1, weight=1)
         self.rowconfigure(5, weight=1)
         self.spell_check_button = Button(self, text='Spell Checker')
         self.spell_check_button.grid(row=0, column=2, sticky=N)

         if self.document_obj.document.is_owner(self.user.info['id']):
             self.invite_button = Button(self, text='Invite')
             self.invite_button.grid(row=1, column=2, sticky=N)

         self.complain_button = Button(self, text='Report this', command=self.handler_complain)
         self.complain_button.grid(row=2, column=2, sticky=N)

         if self.document_obj.document.is_member(self.user.info['id']):
             self.save_button = Button(self, text='Save', command=self.handler_save)
             self.save_button.grid(row=3, column=2, sticky=N)

         self.pack(fill=BOTH, expand=1)

    def handler_save(self):
        #self.textbox_obj.handler_save_file()
        contents = self.document_obj.text_content.get('1.0', END)
        self.document_obj.document.save(contents, self.document_obj.user.info['id'])
        tkMessageBox.showinfo('Saved!', 'The file is saved.')

    def handler_complain(self):
        tkMessageBox.askquestion('d', 'd')
        #doc_id = self.document_obj.document.info['id']
        #print doc_id
        content = 'dummy content'
        self.user.complain(self.doc_id, content, verbose=True)
