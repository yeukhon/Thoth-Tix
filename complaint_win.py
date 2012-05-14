from Tkinter import *
from sqlite3 import connect
from user import User
#from manage import ApplicationManager


class Complaint_Viewer:
    BASE_DIR = 'dbs'

    def __init__(self, master, parent, user):
        self.master = master
        self.user = user
        #self.rows = rows
        self.parent = parent
        #self.manage_App = ApplicationManager()

        self.frame = Frame(master, relief=FLAT)

        self.init_frame_pending()
        self.frame_pending.grid()

        self.frame_quit = Button(
            self.frame,
            text='Home',
            command=self.handler_goto_homepage)
        self.frame_quit.grid()
        return

    def init_frame_pending(self):
        self.frame_pending = LabelFrame(
            self.frame,
            text='Pending Complaints')
        self.frame_pending.columnconfigure(0, weight=2)
        self.frame_pending.columnconfigure(1, weight=2)
        self.frame_pending.columnconfigure(2, weight=22)
        self.frame_pending.columnconfigure(3, weight=2)
        self.frame_pending.columnconfigure(4, weight=1)
        self.frame_pending.columnconfigure(5, weight=1)

        self.frame_pending_header_docid = Label(
            self.frame_pending,
            text='docid')
        self.frame_pending_header_docid.grid(row=0, column=0)

        self.frame_pending_header_docname = Label(
            self.frame_pending,
            text='Title')
        self.frame_pending_header_docname.grid(row=0, column=1)

        self.frame_pending_header_reason = Label(
            self.frame_pending,
            text='Reason')
        self.frame_pending_header_reason.grid(row=0, column=2)

        self.frame_pending_header_actions = Label(
            self.frame_pending,
            text='Actions')
        self.frame_pending_header_actions.grid(row=0, column=3, columnspan=2)

    def handler_goto_homepage(self):
        self.frame.grid_remove()
        self.parent.frame.grid_remove()
        self.parent.init_frame(self.master)
        self.parent.frame.grid()
