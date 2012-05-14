import Tix
import Tkinter as tk
import tkMessageBox
from user import Guest, RegularUser, SuperUser
from textbox import TextBox
from document import Document
from docui_buttons import DocSideButtons
from docui_search import DocSearchUI


class Homepage:

    def __init__(self, master, user):
        # Save a copy of the master window.
        self.master = master
        self.user = user

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

        # Create the notebook widget.
        self.nb = Tix.NoteBook(master, name='nb', ipadx=6, ipady=6,
            width=400, height=400)

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
        f.btns.save.pack(side=Tix.LEFT, padx=2, pady=2, fill=Tix.Y)

        f.btns.close = Tix.Button(f.btns, text='Close', command=self.handler_close_document)
        f.btns.close.pack(side=Tix.RIGHT, padx=2, pady=2, fill=Tix.Y)

        f.tb = TextBox(f, f)
        f.tb.initialize(self.user, Document(docid))
        f.tb.frame.pack(side=Tix.TOP, padx=2, pady=2, fill=Tix.BOTH, expand=1)

        f.dsb = DocSideButtons(f, f.tb, self.user)
        f.dsb.pack(side=Tix.TOP, padx=2, pady=2, fill=Tix.BOTH, expand=1)

        tab.f = f
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

            self.nb.delete('login')
            self.nb.delete('reg')

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
        else:
            tkMessageBox.showerror('Failed', 'Approval failed.')
        return

    def handler_disapprove_app(self, rowid):
        res = self.user.deny_application(rowid)
        if res:
            tkMessageBox.showinfo('Success', 'User has been denied!')
            self.nb.delete('application')
            self.handler_page_applications()
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
        else:
            tkMessageBox.showerror('Failed', 'Membership failed.')
        return

    def handler_open_document(self, docid):
        try:
            self.nb.add('editor', label="Editor", underline=0)
            self.create_page_editor(self.nb, docid)
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
            lb = LabelButton(shl.hlist, label=row['name'], button='View',
                command=lambda i=row['id']: self.update_directory(i))
            shl.hlist.add('D%s' % row['id'], itemtype=Tix.WINDOW, window=lb)

        for row in files:
            lb = LabelButton(shl.hlist, label=row['name'], button='View',
                command=lambda i=row['id']: self.handler_open_document(i))
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
