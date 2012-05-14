import Tix
import Tkinter as tk
import tkMessageBox
from user import Guest, RegularUser, SuperUser
from textbox import TextBox
from document import Document
from docui_buttons import DocSideButtons
from docui_search import DocSearchUI
from historyui import HistoryUI
import re


class Homepage:

    def __init__(self, master, user):
        # Save a copy of the master window.
        self.master = master
        self.user = user

        master.title('Thoth')

        # We use these options to set the sizes of the subwidgets inside the
        # notebook, so that they are well-aligned on the screen.
        prefix = Tix.OptionName(master)
        if prefix:
            prefix = '*'+prefix
        else:
            prefix = ''
        master.option_add(prefix+'*TixControl*entry.width', 10)
        master.option_add(prefix+'*TixControl*label.width', 18)
        master.option_add(prefix+'*TixControl*label.anchor', Tix.E)
        master.option_add(prefix+'*TixNoteBook*tagPadX', 8)

        self.logout = Tix.Button(master, text='Logout',
            command=self.handler_logout)

        # Create the notebook widget.
        self.nb = Tix.NoteBook(master, name='nb', ipadx=6, ipady=6,
            width=600, height=400)

        # Create the two tabs on the notebook. The -underline option
        # puts a underline on the first character of the labels of the tabs.
        # Keyboard accelerators will be defined automatically according
        # to the underlined character.
        self.nb.add('login', label="Login", underline=0)
        self.nb.add('reg', label="Register", underline=0)
        self.nb.add('directory', label="Directory", underline=0)

        self.nb.pack(expand=1, fill=Tix.BOTH, padx=5, pady=5 ,side=Tix.TOP)

        self.create_page_login(self.nb)
        self.create_page_register(self.nb)
        self.create_page_directory(self.nb)

        return

    def create_page_login(self, nb):
        tab = nb.login
        f = Tix.Frame(tab)
        f.pack(side=Tix.LEFT, padx=2, pady=2, fill=Tix.BOTH, expand=1)

        f.msg = Tix.Label(f, text="""Welcome, Please Log in!""",
            wraplength=200)
        f.msg.pack(side=Tix.TOP, padx=2, pady=2, fill=Tix.BOTH, expand=2)

        f.name = Tix.LabelEntry(f, label='Username:', labelside=Tix.LEFT)
        f.name.label.config(width=10)
        f.name.entry.config(width=10)
        f.name.pack(side=Tix.TOP, padx=2, pady=2, fill=Tix.X, expand=1)

        f.pwd = Tix.LabelEntry(f, label='Password:', labelside=Tix.LEFT)
        f.pwd.label.config(width=10)
        f.pwd.entry.config(width=10)
        f.pwd.entry.config(show="*")
        f.pwd.pack(side=Tix.TOP, padx=2, pady=2, fill=Tix.X, expand=1)

        f.btn = Tix.Button(f, text='Login',
            command=self.handler_login)
        f.btn.pack(side=Tix.TOP, padx=2, pady=2, fill=Tix.X, expand=1)

        nb.login.f = f
        return

    def create_page_register(self, nb):
        tab = nb.reg
        f = Tix.Frame(tab)
        f.pack(side=Tix.LEFT, padx=2, pady=2, fill=Tix.BOTH, expand=1)

        f.msg = Tix.Label(f, text="""Registration:""",
            wraplength=200)
        f.msg.pack(side=Tix.TOP, padx=2, pady=2, fill=Tix.BOTH, expand=2)

        f.name = Tix.LabelEntry(f, label='Username:', labelside=Tix.LEFT)
        f.name.label.config(width=10)
        f.name.pack(side=Tix.TOP, padx=2, pady=2, fill=Tix.X, expand=1)

        f.pwd1 = Tix.LabelEntry(f, label='Password:', labelside=Tix.LEFT)
        f.pwd1.label.config(width=10)
        f.pwd1.entry.config(show="*")
        f.pwd1.pack(side=Tix.TOP, padx=2, pady=2, fill=Tix.X, expand=1)

        f.pwd2 = Tix.LabelEntry(f, label='C. Password:', labelside=Tix.LEFT)
        f.pwd2.label.config(width=10)
        f.pwd2.entry.config(show="*")
        f.pwd2.pack(side=Tix.TOP, padx=2, pady=2, fill=Tix.X, expand=1)

        f.email = Tix.LabelEntry(f, label='Email:', labelside=Tix.LEFT)
        f.email.label.config(width=10)
        f.email.pack(side=Tix.TOP, padx=2, pady=2, fill=Tix.X, expand=1)

        f.cmt = Tix.LabelEntry(f, label='Comment:', labelside=Tix.LEFT)
        f.cmt.label.config(width=10)
        f.cmt.pack(side=Tix.TOP, padx=2, pady=2, fill=Tix.X, expand=1)

        f.btn = Tix.Button(f, text='Register',
            command=self.handler_register)
        f.btn.pack(side=Tix.TOP, padx=2, pady=2, fill=Tix.X, expand=1)

        tab.f = f
        return

    def create_page_directory(self, nb):
        #----------------------------------------
        # Create the directory page
        #----------------------------------------
        # Create two frames: one for the common buttons, one for the
        # other widgets
        #
        dirid = 1
        tab = nb.directory
        tab.f = Tix.Frame(tab)
        tab.f.pack(side=Tix.LEFT, padx=2, pady=2, fill=Tix.BOTH, expand=1)

        tab.f.curr = LabelButton(tab.f, label='', button='Go Up')
        tab.f.curr.label.config(bg='#ADD8E6', width=55)
        tab.f.curr.pack(side=Tix.TOP, padx=20, pady=2, fill=Tix.X, expand=1)

        tab.f.shl = Tix.ScrolledHList(tab.f)
        tab.f.shl.pack(side=Tix.TOP, padx=20, pady=2, fill=Tix.BOTH, expand=1000)
        tab.f.shl.hlist.config(bg='#333333')
        self.update_directory(dirid)
        return

    def create_page_make(self, nb):
        tab = nb.make
        f = Tix.Frame(tab)
        f.pack(side=Tix.LEFT, padx=2, pady=2, fill=Tix.BOTH, expand=1)

        f.msg = Tix.Label(f, text="""The item will be created @ """,
            wraplength=200)
        f.msg.pack(side=Tix.TOP, padx=2, pady=2, fill=Tix.BOTH, expand=2)

        f.mdir = Tix.LabelEntry(f, label='Directory:', labelside=Tix.ACROSSTOP)
        f.bdir = Tix.Button(f, text='Create Directory',
            command=self.handler_create_directory)

        f.mdir.pack(side=Tix.TOP, padx=2, pady=2, fill=Tix.X, expand=1)
        f.bdir.pack(side=Tix.TOP, padx=2, pady=2, fill=Tix.X, expand=1)

        f.mdoc = Tix.LabelEntry(f, label='Document:', labelside=Tix.ACROSSTOP)
        f.bdoc = Tix.Button(f, text='Create Document',
            command=self.handler_create_document)

        f.mdoc.pack(side=Tix.TOP, padx=2, pady=2, fill=Tix.X, expand=1)
        f.bdoc.pack(side=Tix.TOP, padx=2, pady=2, fill=Tix.X, expand=1)

        tab.f = f
        return

    def create_page_control(self, nb):
        tab = nb.control
        f = Tix.Frame(tab)
        f.pack(side=Tix.LEFT, padx=2, pady=2, fill=Tix.BOTH, expand=1)

        f.msg = Tix.Label(f, text="""Control Panel""",
            wraplength=200)
        f.msg.pack(side=Tix.TOP, padx=2, pady=2, fill=Tix.BOTH, expand=2)

        #~ f.app = LabelButton(f, label='Applications', button='View',
            #~ command=self.handler_page_applications)
        #~ f.app.pack(side=Tix.TOP, padx=2, pady=2, fill=Tix.X, expand=1)

        f.inv = LabelButton(f, label='Invitations', button='View',
            command=self.handler_page_invitations)
        f.inv.pack(side=Tix.TOP, padx=2, pady=2, fill=Tix.X, expand=1)

        tab.f = f
        return

    def create_page_applications(self, nb):
        tab = nb.application
        f = Tix.Frame(tab)
        f.pack(side=Tix.LEFT, padx=2, pady=2, fill=Tix.BOTH, expand=1)

        f.shl = Tix.ScrolledHList(f)
        f.shl.pack(side=Tix.TOP, padx=20, pady=2, fill=Tix.BOTH, expand=9)

        rowf = Tix.Frame(f.shl.hlist)
        item = [
            Tix.Label(rowf, text='username', width=10),
            Tix.Label(rowf, text='email', width=20),
            Tix.Label(rowf, text='content', width=30),
            Tix.Label(rowf, text='time', width=20),
            Tix.Label(rowf, text='Accept', width=8),
            Tix.Label(rowf, text='Deny', width=7)
        ]
        for i in item:
            i.pack(side=Tix.LEFT, padx=2, pady=2, fill=Tix.Y, expand=1)
        f.shl.hlist.add('header', itemtype=Tix.WINDOW, window=rowf)

        apps = self.user.manage.manage_Admin.get_pending_applications()
        for row in apps:
            rowf = Tix.Frame(f.shl.hlist)
            item = [
                Tix.Label(rowf, text=row['username'], width=10),
                Tix.Label(rowf, text=row['email'], width=20),
                Tix.Label(rowf, text=row['content'], width=30),
                Tix.Label(rowf, text=row['time'], width=20),
                Tix.Button(rowf, text='Accept',
                    command=lambda i=row['id']:self.handler_approve_app(i)
                ),
                Tix.Button(rowf, text='Deny',
                    command=lambda i=row['id']:self.handler_disapprove_app(i)
                )
            ]
            for i in item:
                i.pack(side=Tix.LEFT, padx=2, pady=2, fill=Tix.Y, expand=1)

            f.shl.hlist.add('A%s' % row['id'], itemtype=Tix.WINDOW, window=rowf)

        tab.f = f
        return

    def create_page_invitations(self, nb):
        tab = nb.invitation
        f = Tix.Frame(tab)
        f.pack(side=Tix.LEFT, padx=2, pady=2, fill=Tix.BOTH, expand=1)

        f.shl = Tix.ScrolledHList(f)
        f.shl.pack(side=Tix.TOP, padx=20, pady=2, fill=Tix.BOTH, expand=9)

        rowf = Tix.Frame(f.shl.hlist)
        item = [
            Tix.Label(rowf, text='Document', width=20),
            Tix.Label(rowf, text='From', width=10),
            Tix.Label(rowf, text='Message', width=30),
            Tix.Label(rowf, text='Time', width=20),
            Tix.Label(rowf, text='Accept', width=8),
            Tix.Label(rowf, text='Deny', width=7)
        ]
        for i in item:
            i.pack(side=Tix.LEFT, padx=2, pady=2, fill=Tix.Y, expand=1)
        f.shl.hlist.add('header', itemtype=Tix.WINDOW, window=rowf)

        invs = self.user.manage.manage_User.get_invitations_to(self.user.info['id'])
        for row in invs:
            rowf = Tix.Frame(f.shl.hlist)
            item = [
                Tix.Label(rowf, text=row['docid'], width=20),
                Tix.Label(rowf, text=row['userid_from'], width=10),
                Tix.Label(rowf, text=row['content'], width=30),
                Tix.Label(rowf, text=row['time'], width=20),
                Tix.Button(rowf, text='Accept',
                    command=lambda i=row['id']:self.handler_approve_inv(i)
                ),
                Tix.Button(rowf, text='Deny',
                    command=lambda i=row['id']:self.handler_disapprove_inv(i)
                )
            ]
            for i in item:
                i.pack(side=Tix.LEFT, padx=2, pady=2, fill=Tix.Y, expand=1)

            f.shl.hlist.add('I%s' % row['id'], itemtype=Tix.WINDOW, window=rowf)

        tab.f = f
        return

    def create_page_editor(self, nb, docid):
        tab = nb.editor
        f = Tix.Frame(tab)
        f.pack(side=Tix.LEFT, padx=2, pady=2, fill=Tix.BOTH, expand=1)

        f.btns = Tix.Frame(f)
        f.btns.pack(side=Tix.TOP, padx=2, pady=2, fill=Tix.X, expand=1)

        f.btns.save = Tix.Button(f.btns, text='Save', command=self.handler_save_document)

        f.btns.spell = Tix.Button(f.btns, text='Spellcheck', command=self.handler_page_spellcheck)

        if self.user.info['usergroup'] != 4:
            f.btns.save.pack(side=Tix.LEFT, padx=2, pady=2)
            f.btns.spell.pack(side=Tix.LEFT, padx=2, pady=2)

        f.btns.close = Tix.Button(f.btns, text='Close', command=self.handler_close_document)
        f.btns.close.pack(side=Tix.RIGHT, padx=2, pady=2)

        f.tb = TextBox(f, f)
        f.document = Document(docid)
        f.tb.initialize(self.user, f.document)
        f.tb.frame.pack(side=Tix.TOP, padx=2, pady=2, fill=Tix.BOTH, expand=1)

        tab.f = f

        self.handler_page_comment()
        if self.user.info['usergroup'] != 4:
            self.handler_page_editorPlus()
            self.handler_page_history(f.document)
        return

    def create_page_editorPlus(self, nb):
        tab = nb.editorPlus
        f = Tix.Frame(tab)
        f.pack(side=Tix.LEFT, padx=2, pady=2, fill=Tix.BOTH, expand=1)

        f.inv = Tix.Frame(f)

        f.inv.name = Tix.LabelEntry(f.inv, label="Enter the user's name:")

        f.inv.bname = Tix.Button(f.inv, text='Invite',
            command=self.handler_invite_user)

        if self.nb.editor.f.tb.document.is_member(self.user.info['id']):
            f.inv.pack(side=Tix.TOP, padx=2, pady=2, fill=Tix.X, expand=1)
            f.inv.name.pack(side=Tix.LEFT, padx=2, pady=2, fill=Tix.X, expand=1)
            f.inv.bname.pack(side=Tix.RIGHT, padx=2, pady=2, fill=Tix.X, expand=1)
            

        f.cmpt = Tix.Frame(f)
        f.cmpt.pack(side=Tix.TOP, padx=2, pady=2, fill=Tix.X, expand=1)

        f.cmpt.text = Tix.LabelEntry(f.cmpt, label="Complaint:")
        f.cmpt.text.pack(side=Tix.LEFT, padx=2, pady=2, fill=Tix.X, expand=1)

        f.cmpt.btext = Tix.Button(f.cmpt, text='Submit',
            command=self.handler_user_complaint)
        f.cmpt.btext.pack(side=Tix.RIGHT, padx=2, pady=2, fill=Tix.X, expand=1)

        pref = nb.editor.f.tb.pref.info
        f.pref = Tix.Frame(f)
        f.pref.pack(side=Tix.TOP, padx=2, pady=2, fill=Tix.X, expand=1)

        f.pref.msg = Tix.Label(f.pref, text='Preferences')
        f.pref.msg.pack(side=Tix.TOP, padx=2, pady=2, fill=Tix.BOTH, expand=1)

        f.pref.lnum = Tix.Checkbutton(f.pref, text='Show Line Numbers.')
        f.pref.lnum.var = Tix.IntVar()
        f.pref.lnum.config(variable=f.pref.lnum.var)
        f.pref.lnum.pack(side=Tix.TOP, padx=2, pady=2, fill=Tix.X, expand=1)

        f.pref.bg = Tix.LabelEntry(f.pref, label='Background Color:')
        f.pref.bg.entry.config(width=7)
        f.pref.bg.pack(side=Tix.TOP, padx=2, pady=2, fill=Tix.X, expand=1)
        
        f.pref.fg = Tix.LabelEntry(f.pref, label='Foreground Color:')
        f.pref.fg.entry.config(width=7)
        f.pref.fg.pack(side=Tix.TOP, padx=2, pady=2, fill=Tix.X, expand=1)

        f.pref.sbg = Tix.LabelEntry(f.pref, label='Select BG Color:')
        f.pref.sbg.entry.config(width=7)
        f.pref.sbg.pack(side=Tix.TOP, padx=2, pady=2, fill=Tix.X, expand=1)
        
        f.pref.sfg = Tix.LabelEntry(f.pref, label='Select FG Color:')
        f.pref.sfg.entry.config(width=7)
        f.pref.sfg.pack(side=Tix.TOP, padx=2, pady=2, fill=Tix.X, expand=1)

        f.pref.fh = Tix.LabelEntry(f.pref, label='Font Height:')
        f.pref.fh.entry.config(width=3)
        f.pref.fh.pack(side=Tix.TOP, padx=2, pady=2, fill=Tix.X, expand=1)

        f.pref.btn = Tix.Button(f.pref, text='Save',
            command=self.handler_save_preferences)
        f.pref.btn.pack(side=Tix.TOP, padx=2, pady=2, fill=Tix.X, expand=1)

        if pref['line_numbers']:
            f.pref.lnum.var.set(1)
        f.pref.bg.entry.insert(0, pref['bg_color'])
        f.pref.fg.entry.insert(0, pref['fg_color'])
        f.pref.sbg.entry.insert(0, pref['select_bg'])
        f.pref.sfg.entry.insert(0, pref['select_fg'])
        f.pref.fh.entry.insert(0, pref['font_height'])

        tab.f = f
        return

    def create_page_comment(self, nb):
        tab = nb.comment
        f = Tix.Frame(tab)
        f.pack(side=Tix.LEFT, padx=2, pady=2, fill=Tix.BOTH, expand=1)

        f.shl = Tix.ScrolledHList(f)
        f.shl.pack(side=Tix.TOP, padx=20, pady=2, fill=Tix.BOTH, expand=9)

        docid = self.nb.editor.f.tb.document.info['id']
        invs = self.nb.editor.f.tb.document.get_document_comments(docid)
        for row in invs:
            rowf = Tix.Frame(f.shl.hlist)
            item = [
                Tix.Label(rowf, text=row['user'], width=10),
                Tix.Label(rowf, text=row['content'], width=30),
                Tix.Label(rowf, text=row['time'], width=20)
            ]

            item[0].pack(side=Tix.LEFT, padx=2, pady=2, fill=Tix.Y, expand=1)
            item[2].pack(side=Tix.RIGHT, padx=2, pady=2, fill=Tix.Y, expand=1)
            item[1].pack(side=Tix.BOTTOM, padx=2, pady=2, fill=Tix.Y, expand=1)

            f.shl.hlist.add('I%s' % row['id'], itemtype=Tix.WINDOW, window=rowf)

        f.cmt = Tix.Frame(f)
        f.cmt.pack(side=Tix.TOP, padx=2, pady=2, fill=Tix.BOTH, expand=1)

        f.cmt.msg = Tix.LabelEntry(f.cmt, label='Leave a comment:', labelside=Tix.TOP)
        f.cmt.msg.pack(side=Tix.TOP, padx=2, pady=2, fill=Tix.BOTH, expand=1)

        f.cmt.bcmt = Tix.Button(f.cmt, text='Submit',
            command=self.handler_user_comment)
        f.cmt.bcmt.pack(side=Tix.RIGHT, padx=2, pady=2, fill=Tix.Y, expand=1)

        tab.f = f
        return

    def create_page_complaint(self, nb):
        tab = nb.complaint
        f = Tix.Frame(tab)
        f.pack(side=Tix.LEFT, padx=2, pady=2, fill=Tix.BOTH, expand=1)

        f.shl = Tix.ScrolledHList(f)
        f.shl.pack(side=Tix.TOP, padx=20, pady=2, fill=Tix.BOTH, expand=9)

        rowf = Tix.Frame(f.shl.hlist)
        item = [
            Tix.Label(rowf, text='ID', width=3),
            Tix.Label(rowf, text='user', width=10),
            Tix.Label(rowf, text='content', width=30),
            Tix.Label(rowf, text='time', width=20)
        ]
        for i in item:
            i.pack(side=Tix.LEFT, padx=2, pady=2, fill=Tix.Y, expand=1)
        f.shl.hlist.add('header', itemtype=Tix.WINDOW, window=rowf)

        invs = self.user.get_all_complaints()
        print 'fewfe', invs
        for row in invs:
            rowf = Tix.Frame(f.shl.hlist)
            item = [
                Tix.Label(rowf, text=row['id'], width=3),
                Tix.Label(rowf, text=row['user'], width=10),
                Tix.Label(rowf, text=row['content'], width=30),
                Tix.Label(rowf, text=row['time'], width=20)
            ]

            item[0].pack(side=Tix.LEFT, padx=2, pady=2, fill=Tix.Y, expand=1)
            item[1].pack(side=Tix.LEFT, padx=2, pady=2, fill=Tix.Y, expand=1)
            item[2].pack(side=Tix.LEFT, padx=2, pady=2, fill=Tix.Y, expand=1)
            item[3].pack(side=Tix.LEFT, padx=2, pady=2, fill=Tix.Y, expand=1)

            f.shl.hlist.add('I%s' % row['id'], itemtype=Tix.WINDOW, window=rowf)

        print 'pass shl'
        f.res = Tix.Frame(f)
        f.res.pack(side=Tix.TOP, padx=2, pady=2, fill=Tix.BOTH, expand=1)
        print 'pass frame'
        f.res.ID = Tix.LabelEntry(f.res, label='ID:', labelside=Tix.LEFT)
        f.res.ID.pack(side=Tix.TOP, padx=2, pady=2, fill=Tix.X, expand=1)
        print 'pass label entr'

        f.res.txt = Tix.LabelEntry(f.res, label='Response:', labelside=Tix.LEFT)
        f.res.txt.pack(side=Tix.TOP, padx=2, pady=2, fill=Tix.X, expand=1)
        print 'pass txt'
        f.res.btny = Tix.Button(f.res, text='Valid',
            command=self.handler_approve_complaint)
        f.res.btny.pack(side=Tix.LEFT, padx=2, pady=2, fill=Tix.Y, expand=1)

        f.res.btnn = Tix.Button(f.res, text='Invalid',
            command=self.handler_disapprove_complaint)
        f.res.btnn.pack(side=Tix.RIGHT, padx=2, pady=2, fill=Tix.Y, expand=1)
        print 'pass butn'
        tab.f = f
        return

    def create_page_history(self, nb, document):
        tab = nb.history
        f = Tix.Frame(tab)
        f.pack(side=Tix.LEFT, padx=2, pady=2, fill=Tix.BOTH, expand=1)
        print 'pass hisf'
        f.history = HistoryUI(f, document)
        f.history.frame.pack(side=Tix.TOP, padx=2, pady=2, fill=Tix.BOTH, expand=1)

        tab.f = f
        return

    def create_page_spellcheck(self, nb):
        tab = nb.spell
        f = Tix.Frame(tab)
        f.pack(side=Tix.LEFT, padx=2, pady=2, fill=Tix.BOTH, expand=1)
        print 'pass frame'
        f.dic = self.nb.editor.f.tb.spellcheck
        
        f.msg = Tix.Message(f, text='')
        
        f.sug = Tix.Frame(f)
        
        f.btns = Tix.ButtonBox(f, orientation=Tix.VERTICAL)
        print 'pass vert'
        f.btns.add('change', text='Change',
            command=self.handler_spellcheck_change)
        print 'pass change'
        f.btns.add('add', text='Add to Dic',
            command=self.handler_spellcheck_add)
        f.btns.add('next', text='Next',
            command=self.handler_spellcheck_next)
        
        print 'pass pack'
        tab.f = f
        self.handler_spellcheck_next()
        return

    def handler_login(self, event=0):
        # Get the username the user typed.
        name = self.nb.login.f.name.entry.get()
        # Get the password the user typed and md5 it.
        password = self.nb.login.f.pwd.entry.get()

        # Check for the user in the database.
        res = self.user.login(name, password)

        # If the supplied user is in the database:
        if res:
            res = res[-1]
            if res['usergroup'] == 1:
                # Update the User instance with the new user information.
                self.user = SuperUser(userid=res['id'])

                self.nb.add('control', label="Control", underline=0)
                self.create_page_control(self.nb)
                self.nb.add('application', label="Apps", underline=0)
                self.create_page_applications(self.nb)
                self.handler_page_complaint()
            else:
                # Update the User instance with the new user information.
                self.user = RegularUser(userid=res['id'])
                self.nb.add('make', label="Make", underline=0)
                self.create_page_make(self.nb)
                self.update_directory(1)

                self.nb.add('control', label="Control", underline=0)
                self.create_page_control(self.nb)

            # Reset the username and password field.
            self.nb.login.f.name.entry.delete(0, len(name))
            self.nb.login.f.pwd.entry.delete(0, len(password))

            self.nb.pack_forget()
            self.logout.pack(side=Tix.TOP, padx=2, pady=2)
            self.nb.pack(side=Tix.TOP, padx=5, pady=5, fill=Tix.BOTH, expand=1)

            self.nb.delete('login')
            try:
                self.nb.delete('reg')
            except:
                pass
            self.nb.raise_page('directory')

            tkMessageBox.showinfo(
                'Authenticated', 'Welcome back! Logged in as %s' %res['username'])

        # The supplied username is not in the database.
        else:
            # Reset the username and password field.
            self.nb.login.f.name.entry.delete(0, len(name))
            self.nb.login.f.pwd.entry.delete(0, len(password))
        return

    def handler_register(self):
        username = self.nb.reg.f.name.entry.get()
        password_1 = self.nb.reg.f.pwd1.entry.get()
        password_2 = self.nb.reg.f.pwd2.entry.get()
        email = self.nb.reg.f.email.entry.get()
        content = self.nb.reg.f.cmt.entry.get()

        user_exist = self.user.manage.manage_DB.get_info('user', where={
                'username': username})
        if username and email and password_1 and password_2 \
            and content and not user_exist:
             if password_1 == password_2:
                 res = Guest().register(username, password_1, email, content)
                 tkMessageBox.showinfo('Successful', "You have just signed up an account. Please wait for system admin to approve your application. Thank you.")

                 self.nb.delete('reg')
                 self.nb.raise_page('login')

             else:
                 tkMessageBox.showerror('Password do not match', 'The passwords you entered do not match. Try again!')
             return False
        elif user_exist:
             tkMessageBox.showerror('Failed', 'Username already taken. Please another one.')
             return False
        else:
             tkMessageBox.showerror('Failed', 'Please enter all the information correctly.')
             return False

    def handler_create_directory(self):
        # The user is of the 'Regular Users' or 'Super User' usergroup.
        if self.user.info['usergroup'] <= 2:
            # Get the name of the directory the user wants to create.
            name = self.nb.make.f.mdir.entry.get()
            # Create a new directory.
            res = self.user.create_new_directory(name, self.directory['id'])

            # If the directory was created:
            if res:
                # Delete the directory name from the creation box.
                self.nb.make.f.mdir.entry.delete(0, len(name))
                # Update the display to show the newly created directory.
                self.update_directory(self.directory['id'])
                tkMessageBox.showinfo(
                    'Success',
                    'Directory "' + name +
                    '" was created!')
                self.nb.raise_page('directory')
            # Else the directory was not created:
            else:
                # Show the appropriate error message.
                tkMessageBox.showerror(
                    'Error Creating Directory!',
                    'Directory "' + name +
                    '" cannot be created at this time!')
        # User is of the 'Suspended' usergroup.
        elif self.user.info['usergroup'] == 3:
            # Show the appropriate error message.
            tkMessageBox.showerror(
                'Insufficient Privileges',
                'Your account has been suspended!')
        # User is of the 'Visitor' usergroup.
        else:
            # Show the appropriate error message.
            tkMessageBox.showerror(
                'Insufficient Privileges',
                'You must login before you can preform this action!')
        return

    def handler_create_document(self):
        # The user is of the 'Regular Users' or 'Super User' usergroup.
        if self.user.info['usergroup'] <= 2:
            # Get the name of the document the user wants to create.
            name = self.nb.make.f.mdoc.entry.get()
            # Create a document at the current directory.
            res = self.user.create_new_document(name, self.directory['id'])

            # If the document was created:
            if res:
                # Delete the document name from the creation box.
                self.nb.make.f.mdoc.entry.delete(0, len(name))
                # Update the display to show the newly created document.
                self.update_directory(self.directory['id'])
                tkMessageBox.showinfo(
                    'Success',
                    'Document "' + name +
                    '" was created!')
                self.nb.raise_page('directory')
            # Else the document was not created:
            else:
                # Show the appropriate error message.
                tkMessageBox.showerror(
                    'Error Creating Document!',
                    'Document "' + name +
                    '" cannot be created at this time!')
        # User is of the 'Suspended' usergroup.
        elif self.user.info['usergroup'] == 3:
            # Show the appropriate error message.
            tkMessageBox.showerror(
                'Insufficient Privileges',
                'Your account has been suspended!')
        # User is of the 'Visitor' usergroup.
        else:
            # Show the appropriate error message.
            tkMessageBox.showerror(
                'Insufficient Privileges',
                'You must login before you can preform this action!')

        return

    def handler_page_applications(self):
        try:
            self.nb.add('application', label="Apps", underline=0)
            self.create_page_applications(self.nb)
            return
        except:
            return

    def handler_page_invitations(self):
        try:
            self.nb.add('invitation', label="Invite", underline=0)
            self.create_page_invitations(self.nb)
            return
        except:
            return

    def handler_approve_app(self, rowid):
        res = self.user.accept_application(rowid)
        if res:
            tkMessageBox.showinfo('Success', 'User has been created!')
            self.nb.delete('application')
            self.handler_page_applications()
            self.nb.raise_page('application')
        else:
            tkMessageBox.showerror('Failed', 'Approval failed.')
        return

    def handler_disapprove_app(self, rowid):
        res = self.user.deny_application(rowid)
        if res:
            tkMessageBox.showinfo('Success', 'User has been denied!')
            self.nb.delete('application')
            self.handler_page_applications()
            self.nb.raise_page('application')
        else:
            tkMessageBox.showerror('Failed', 'Denial failed.')
        return

    def handler_approve_inv(self, docid):
        res = self.user.manage.manage_DB.insert_info('member',
            insert={'userid':self.user.info['id'], 'docid':docid})
        if res:
            res = self.user.manage.manage_DB.update_info('invitation',
                update={'status':1}, where={'userid_to':self.user.info['id'],
                'docid':docid})
            if res:
                tkMessageBox.showinfo('Success', 'You are a member of the document!')
                self.nb.delete('invitation')
                self.handler_page_invitations()
                self.nb.raise_page('invitation')
            else:
                tkMessageBox.showerror('Failed', 'Updating Membership failed.')
        else:
            tkMessageBox.showerror('Failed', 'Membership failed.')
        return

    def handler_disapprove_inv(self, docid):
        res = self.user.manage.manage_DB.update_info('invitation',
            update={'status':-1}, where={'userid_to':self.user.info['id'],
            'docid':docid})
        if res:
            tkMessageBox.showinfo('Success', 'You are not a member of the document!')
            self.nb.delete('invitation')
            self.handler_page_invitations()
            self.nb.raise_page('invitation')
        else:
            tkMessageBox.showerror('Failed', 'Membership failed.')
        return

    def handler_open_document(self, docid):
        try:
            self.nb.add('editor', label="Editor", underline=0)
            self.create_page_editor(self.nb, docid)
            self.nb.raise_page('editor')
            return
        except:
            return

    def handler_save_document(self):
        content = self.nb.editor.f.tb.text_content.get('1.0', tk.END)
        userid = self.user.info['id']
        self.nb.editor.f.tb.document.save(content, userid)
        return

    def handler_close_document(self):
        self.nb.delete('editor')
        self.nb.delete('comment')
        if self.user.info['usergroup'] != 4:
            self.nb.delete('editorPlus')
            self.nb.delete('history')
        self.nb.raise_page('directory')
        return

    def handler_page_history(self, document):
        print 'pass hand'
        try:
            self.nb.add('history', label="History", underline=0)
            self.create_page_history(self.nb, document)
            return
        except:
            return

    def handler_page_editorPlus(self):
        try:
            self.nb.add('editorPlus', label="Editor+")
            self.create_page_editorPlus(self.nb)
            return
        except:
            return

    def handler_invite_user(self):
        name = self.nb.editorPlus.f.inv.name.entry.get()
        if not name:
            return

        res = self.user.manage.manage_DB.get_info('user',
            where={'username': name})

        if res and name.lower() != self.user.info['username'].lower():
            content = 'I am inviting you to become a contributor of this document.'
            docid = self.nb.editor.f.tb.document.info['id']
            self.user.send_invitation_to(docid, res[-1]['id'], content)
            self.nb.editorPlus.f.inv.name.entry.delete(0, len(name))
            tkMessageBox.showinfo('Invitation', 'Invitation sent to %s.' % name)
        else:
            if name.lower() == self.user.info['username'].lower():
                tkMessageBox.showerror('Invitation', 'You cannot invite yourself.')
            else:
                tkMessageBox.showerror('Invitation', 'The username does not exist!')

    def handler_user_comment(self):
        content = self.nb.comment.f.cmt.msg.entry.get()
        if not content:
            return

        docid = self.nb.editor.f.tb.document.info['id']
        res = self.user.comment(docid, content)

        if res:
            self.nb.delete('comment')
            self.handler_page_comment()
            self.nb.raise_page('comment')
            tkMessageBox.showinfo('Succes', 'Comment was added.')
        else:
            tkMessageBox.showerror('Failure', 'Your comment was not added.')

        return

    def handler_page_comment(self):
        try:
            self.nb.add('comment', label="Comments")
            self.create_page_comment(self.nb)
            return
        except:
            return

    def handler_user_complaint(self):
        content = self.nb.editorPlus.f.cmpt.text.entry.get()
        if not content:
            return

        docid = self.nb.editor.f.tb.document.info['id']
        res = self.user.complain(docid, content)

        if res:
            self.nb.editorPlus.f.cmpt.text.entry.delete(0, len(content))
            tkMessageBox.showinfo('Succes', 'Complaint was sent to the Admin.')
        else:
            tkMessageBox.showerror('Failure', 'Your complaint was not sent.')

        return

    def handler_page_complaint(self):
        try:
            self.nb.add('complaint', label="Complaint")
            self.create_page_complaint(self.nb)
            return
        except:
            return

    def handler_approve_complaint(self):
        ID = self.nb.complaint.f.res.ID.entry.get()
        if re.match('\d+', ID):
            ID = int(ID)
            res = self.user.manage.manage_DB.get_info('complaint', rowid=ID)
            if res:
                text = self.nb.complaint.f.res.txt.entry.get()
                self.user.response_complaint(ID, 1, text)

                self.nb.delete('complaint')
                self.handler_page_complaint()
                self.nb.raise_page('complaint')
                tkMessageBox.showinfo('Success', 'Response was sent.')
        else:
            tkMessageBox.showerror('Failed', 'ID must be a number.')

        return

    def handler_disapprove_complaint(self):
        ID = self.nb.complaint.f.res.ID.entry.get()
        if re.match('\d+', ID):
            ID = int(ID)
            res = self.user.manage.manage_DB.get_info('complaint', rowid=ID)
            if res:
                text = self.nb.complaint.f.res.txt.entry.get()
                self.user.response_complaint(ID, -1, text)

                self.nb.delete('complaint')
                self.handler_page_complaint()
                tkMessageBox.showinfo('Success', 'Response was sent.')
        else:
            tkMessageBox.showerror('Failed', 'ID must be a number.')

    def handler_save_preferences(self):
        pref = self.nb.editorPlus.f.pref
        info = self.nb.editor.f.tb.pref.info
        
        if pref.lnum.var.get() == 1:
            info['line_numbers'] = True
        else:
            info['line_numbers'] = False
            
        if re.match('\#[0-9a-fA-F]{6}', pref.bg.entry.get()):
            info['bg_color'] = pref.bg.entry.get()
        else:
            tkMessageBox.showerror('Failed', 'Background color is invalid!')
            return

        if re.match('\#[0-9a-fA-F]{6}', pref.fg.entry.get()):
            info['fg_color'] = pref.fg.entry.get()
        else:
            tkMessageBox.showerror('Failed', 'Foreground color is invalid!')
            return

        if re.match('\#[0-9a-fA-F]{6}', pref.sbg.entry.get()):
            info['select_bg'] = pref.sbg.entry.get()
        else:
            tkMessageBox.showerror('Failed', 'Select background color is invalid!')
            return

        if re.match('\#[0-9a-fA-F]{6}', pref.sfg.entry.get()):
            info['select_bg'] = pref.sfg.entry.get()
        else:
            tkMessageBox.showerror('Failed', 'Select foreground color is invalid!')
            return

        if re.match('\d+', pref.fh.entry.get()):
            info['font_height'] = int(pref.fh.entry.get())
        else:
            tkMessageBox.showerror('Failed', 'Font size is invalid!')
            return

        self.nb.editor.f.tb.pref.save()
        self.nb.editor.f.tb.update_preferences()
        tkMessageBox.showinfo('Success', 'Preferences were saved!')

    def handler_page_spellcheck(self):
        try:
            self.nb.add('spell', label="SpellCheck")
            self.create_page_spellcheck(self.nb)
            return
        except:
            return

    def handler_spellcheck_change(self):
        tb = self.nb.editor.f.tb.text_content
        wrong = self.nb.spell.f.cur[0]
        sug = self.nb.spell.f.sug.var.get()
        index = tb.search(wrong, '0.0', nocase=1)
        while index != '':
            tb.delete(index, '%s +%sc' % (index, len(wrong)))
            tb.insert(index, sug)
            index = tb.search(wrong, '0.0', nocase=1)

        tkMessageBox.showinfo('Success', 'The word was replaced in the editor!')
        self.handler_spellcheck_next()
        return

    def handler_spellcheck_add(self):
        wrong = self.nb.spell.f.cur[0]
        userid = self.user.info['id']
        res = self.user.manage.manage_DB.insert_info('X%s' % userid, insert={'word': wrong})

        if res:
            tkMessageBox.showinfo('Success', 'The word was added to your dictionary!')
        else:
            tkMessageBox.showerror('Success', 'The word was not added your dictionary!')
        self.handler_spellcheck_next()

    def handler_spellcheck_next(self):
        f = self.nb.spell.f
        f.msg.pack_forget()
        f.sug.pack_forget()
        f.btns.pack_forget()
        print 'pass forget'
        if len(f.dic) == 0:
            f.msg.config(text='There are no misspellings.')
            f.msg.pack(side=Tix.TOP, padx=2, pady=2, fill=Tix.BOTH, expand=1)

            return

        f.cur = f.dic.popitem()
        print 'pass dic'
        f.msg.config(text=f.cur[0])
        f.msg.pack(side=Tix.TOP, padx=2, pady=2, fill=Tix.BOTH, expand=1)
        print 'pass msg'
        f.sug = Tix.Frame(f)
        f.sug.pack(side=Tix.LEFT, padx=2, pady=2, fill=Tix.BOTH, expand=1)
        print 'pass sug frame'
        f.sug.var = Tix.StringVar()
        f.sug.arr = []
        print 'pass svar'
        for i in f.cur[1]:
            f.sug.arr.append(Tix.Radiobutton(f.sug, text=i['word'], value=i['word'], variable=f.sug.var))
            f.sug.arr[-1].pack(side=Tix.TOP, padx=2, pady=2, fill=Tix.BOTH, expand=1)
        
        f.btns.pack(side=Tix.RIGHT, padx=2, pady=2, fill=Tix.BOTH, expand=1)

    def handler_logout(self):
        self.user = Guest()

        try:
            self.nb.delete('make')
        except:
            pass

        try:
            self.nb.delete('control')
        except:
            pass
            
        try:
            self.nb.delete('editor')
            self.nb.delete('comment')
        except:
            pass

        try:
            self.nb.delete('editorPlus')
            self.nb.delete('history')
        except:
            pass

        try:
            self.nb.delete('invitation')
        except:
            pass
        try:
            self.nb.delete('complaint')
        except:
            pass

        try:
            self.nb.delete('application')
        except:
            pass
            
        self.logout.pack_forget()

        self.nb.add('login', label="Login", underline=0)
        self.nb.add('reg', label="Register", underline=0)

        self.create_page_login(self.nb)
        self.create_page_register(self.nb)
        self.nb.raise_page('directory')
        return

    def update_directory(self, dirid):
        if dirid == 0:
            return

        tab = self.nb.directory
        curr = tab.f.curr
        shl = tab.f.shl
        shl.hlist.delete_all()

        self.directory = self.user.manage.manage_DB.get_info('directory',
            rowid=dirid)
        curr.config(label=self.directory['name'],
            command=lambda i=self.directory['parent_dir']:
            self.update_directory(i))

        folders = self.user.manage.manage_Dirs.get_directory_directories(dirid)
        files = self.user.manage.manage_Docs.get_directory_documents(dirid)

        for row in folders:
            lb = LabelButton(shl.hlist, label='Folder: %s' % row['name'], button='View', 
                command=lambda i=row['id']: self.update_directory(i))
            lb.label.config(bg='#A020F0', width=55)
            shl.hlist.add('D%s' % row['id'], itemtype=Tix.WINDOW, window=lb)

        for row in files:
            lb = LabelButton(shl.hlist, label='File: %s' % row['name'], button='View',
                command=lambda i=row['id']: self.handler_open_document(i))
            lb.label.config(bg='#90EE90', width=55)
            shl.hlist.add('F%s' % row['id'], itemtype=Tix.WINDOW, window=lb)

        try:
            # Get the logical path for the supplied directory.
            path_logical = self.user.manage.manage_Dirs.get_directory_path(
                self.directory['id'])[0]
            self.nb.make.f.msg.config(text="""The item will be created @ %s""" % path_logical)
        except:
            return
        return

class LabelButton(Tix.Frame):

    def __init__(self, master, label='', button='', command=None):
        self.master = master

        # Initialize the parent class.
        Tix.Frame.__init__(self, master)

        self.label = Tix.Label(self, text=label)
        self.button = Tix.Button(self, text=button, command=command)

        self.label.pack(side=Tix.LEFT, padx=2, pady=2, fill=Tix.Y)
        self.button.pack(side=Tix.RIGHT, padx=2, pady=2, fill=Tix.Y)

        return

    def config(self, label=None, button=None, command=None):
        if label != None:
            self.label.config(text=label)

        if button != None:
            self.button.config(text=button)

        if command != None:
            self.button.config(command=command)

        return


if __name__ == '__main__':
    root = Tix.Tk()
    from user import Guest
    gu = Guest()
    Homepage(root, gu)
    root.mainloop()
