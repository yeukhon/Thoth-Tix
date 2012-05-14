from Tkinter  import *
from user import User, Guest
import tkMessageBox
from invitation_win import Invitation_Viewer_Window
from application_win import App_Viewer_Window
from login_win import Login_Window
from textbox import TextBox
from manage import DocumentManager
from document import Document
#from docui import DocUI
from docui_buttons import DocSideButtons
from docui_search import DocSearchUI
from register_window import Register_Window
from docui_search_box import DocSearchBox
from status_bar import StatusBar
from complaint_win import Complaint_Viewer

class Homepage:
    BASE_DIR = 'dbs'

    def __init__(self, master, user):
        self.user = user
        self.master = master
        self.user.manage.manage_DB.check()
        self.manage_Docs = DocumentManager(self.user.manage.manage_DB)

        # Child Windows:
        #self.window_login = Login_Window(master, self, self.user)
        #self.register_window = Register_Window(master, self, self.user)

        #self.window_eitor = TextBox(master, self)
        self.window_invitations = Invitation_Viewer_Window(
            master, self, self.user)
        #self.window_applications = App_Viewer_Window(master, self, self.user)

        self.directory = {'name': '', 'parent_dir': '1'}
        self.directory_contents = []

        self.font = ("Helvetica", "20", "normal")

        self.top = master.winfo_toplevel()
        self.init_frame(master)
        self.window_login = Login_Window(master, self, self.user)
        self.register_window = Register_Window(master, self, self.user)
        self.init_menus()
        return

    def init_frame(self, master):
        self.frame = Frame(master, relief=FLAT)
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)
        self.frame.columnconfigure(2, weight=1)

        self.init_frame_directory()
        self.init_frame_create()
        self.init_frame_cpanel()
        self.update_directory(1)

        self.frame_dir.grid(row=0, column=0, sticky=N + E + S + W, padx="20px", pady="10px")
        self.frame_create.grid(row=1, column=0, sticky=N + E + S + W, padx="20px", pady="10px")
        self.frame_cpanel.grid(row=0, column=1, rowspan=2, sticky=N + E + S + W, padx="20px", pady="10px")

        self.frame_sb = Frame(master, self.frame)
        self.frame_sb.grid(row=3, column=0, sticky=W+E)
        #self.statusbar = StatusBar(self.frame_sb)
        #self.statusbar.pack(side=BOTTOM,fill=X)
        #self.statusbar.grid(row=0, column=0, sticky=W+E)
        #self.l = Label(self.frame_sb, text='JSDFSD')
        #self.l.grid()
        self.status = StringVar()
        self.label = Label(self.frame_sb, relief=SUNKEN, anchor=W, textvariable=self.status)
        self.status.set('Running..')
        self.label.pack(fill=X)
        return

    def init_frame_directory(self):
        # Left Side Frame.
        self.frame_dir = LabelFrame(
            self.frame,
            text='Directory Files:')
        self.frame_dir.columnconfigure(0, weight=30)
        self.frame_dir.columnconfigure(1, weight=1)

        # Displays the current directory
        self.frame_directory_label = Label(
            self.frame_dir,
            text=self.directory['name'] + '/',
            fg='#ffa500', bg='#333')
        self.frame_directory_label.grid(
            row=1, column=0, sticky=N + E + S + W)

        # Button to go up a directory
        self.frame_dir_ctrl_up = Button(
            self.frame_dir,
            text='Up',
            width=4,
            padx=1,
            relief=RAISED,
            command=self.handler_directory_up)
        self.frame_dir_ctrl_up.grid(row=1, column=1, sticky=N + E + S + W)

        return

    def init_frame_create(self):
        # Create file and directory frame
        self.frame_create = LabelFrame(
            self.frame,
            text='Creation:')
        self.frame_create.columnconfigure(0, weight=30)
        self.frame_create.columnconfigure(1, weight=1)

        # Create Directory
        self.frame_create_banner_dir = Label(
            self.frame_create)
        self.frame_create_banner_dir.grid(
            row=0, column=0, columnspan=2, sticky=N + S + W)

        self.entry_dirname = Entry(self.frame_create)
        self.entry_dirname.grid(row=1, column=0, sticky=N + E + S + W)
        self.button_dirname = Button(
            self.frame_create,
            text='Create',
            width=5,
            padx=1,
            relief=RAISED,
            command=self.handler_create_directory)
        self.button_dirname.grid(row=1, column=1, sticky=N + E + S + W)

        # Create Document
        self.frame_create_banner_doc = Label(
            self.frame_create)
        self.frame_create_banner_doc.grid(
            row=2, column=0, columnspan=2, sticky=N + S + W)

        self.entry_docname = Entry(self.frame_create)
        self.entry_docname.grid(row=3, column=0, sticky=N + E + S + W)
        self.button_docname = Button(
            self.frame_create,
            text='Create',
            width=5,
            padx=1,
            relief=RAISED,
            command=self.handler_create_document)
        self.button_docname.grid(row=3, column=1, sticky=N + E + S + W)

        return

    def init_frame_cpanel(self):
        self.frame_cpanel = LabelFrame(self.frame, text='Control Panel:')
        self.frame_cpanel.columnconfigure(0, weight=1)

        self.frame_cpanel_user = Label(
            self.frame_cpanel,
            text=self.user.info['username'],
            fg='#ffa500', bg='#333')
        self.frame_cpanel_user.grid(sticky=N + E + S + W)
        group_id = self.user.info['usergroup']

        if group_id == 1:
            #results = self.user.manage.manage_DB.get_info('application', where={'status':0})
            self.window_applications = App_Viewer_Window(self.master, self, self.user)
            self.frame_cpanel_application = Button(
               self.frame_cpanel, text='Approve User',
               width=11,
               relief=RAISED,
               command=self.handler_view_applications)
            self.frame_cpanel_application.grid()
            self.complaint_applications = Complaint_Viewer(self.master, self, self.user)
            self.frame_cpanel_complaint = Button(
               self.frame_cpanel, text='Manage Complaints',
               width=11,
               relief=RAISED,
               command=self.handler_view_complaints)
            self.frame_cpanel_complaint.grid()

        # View Your Documents Button
        self.frame_cpanel_ownerdocs = Button(
            self.frame_cpanel,
            text='Documents',
            width=11,
            relief=RAISED)
        self.frame_cpanel_ownerdocs.grid()

        # View Invitations Button
        self.frame_cpanel_invitations = Button(
            self.frame_cpanel,
            text='Invitations',
            width=11,
            relief=RAISED,
            command=self.handler_view_invitations)
        self.frame_cpanel_invitations.grid()

        # Search Button
        self.frame_cpanel_search = Button(
            self.frame_cpanel,
            text='Search',
            width=11,
            relief=RAISED)
        self.frame_cpanel_search.grid()

        # View Complaints Button
        self.frame_cpanel_complaints = Button(
            self.frame_cpanel,
            text='Complaints',
            width=11,
            relief=RAISED)
        self.frame_cpanel_complaints.grid()

        return

    def init_menus(self):
        # Create the menubar that will hold all the menus and thier items.
        self.menubar = Menu(self.frame)

        # File Pulldown menu, contains "Open", "Save", and "Exit" options.
        self.loginmenu = Menu(self.menubar, tearoff=0)

        # If the current user is a Guest:
        if self.user.info['usergroup'] == 4:
            # Create the login and register menu options.
            self.loginmenu.add_command(label="Login", command=self.handler_view_login)
            self.loginmenu.add_command(label="Register", command=self.handler_view_register)
            self.loginmenu.add_separator()
            self.loginmenu.add_command(label="Exit", command=self.handler_exit)
            self.menubar.add_cascade(label="Login/Register", menu=self.loginmenu)
        # Else the current user is the SuperUser or RegularUser:
        elif self.user.info['usergroup'] <= 2:
            self.loginmenu.add_command(label="Logout", command=self.handler_view_logout)
            self.loginmenu.add_command(label="My Documents", command=self.handler_view_my_doc)
            self.loginmenu.add_separator()
            self.loginmenu.add_command(label="Exit", command=self.handler_exit)
            self.menubar.add_cascade(label="My Account", menu=self.loginmenu)

        self.helpmenu = Menu(self.menubar, tearoff=0)
        self.helpmenu.add_command(label="Get Help", command=self.show_help)
        self.helpmenu.add_command(label="About", command=self.show_about)
        self.menubar.add_cascade(label="Help", menu=self.helpmenu)

        self.top["menu"] = self.menubar
        return

    def update_directory(self, directoryid):
        # Get the information for the supplied directory.
        self.directory = self.user.manage.manage_DB.get_info('directory',
            rowid=directoryid)

        # Get a list of the directories in the supplied directory.
        self.directory_dir = self.user.manage.manage_Dirs.get_directory_directories(directoryid)
        # Get a list of the documents in the supplied directory.
        self.directory_doc = self.manage_Docs.get_directory_documents(directoryid)


        # Remove the labels from the previous directory from the grid.
        for label in self.directory_contents:
            label[0].grid_remove()
            label[1].grid_remove()
        # Reset the directory contents list to empty.
        self.directory_contents = []

        # Display the current directory.
        self.frame_directory_label.configure(
            text=self.directory['name'] + '/')

        # Contents of the directory start on row 2.
        start = 2
        for row in self.directory_dir:
            # Each entry of the directory_contents list will be the entire row
            # of the grid. Each row is composed of a Label for that directory
            # and a Button to move into that directory.
            self.directory_contents.append([
                Label(
                    self.frame_dir,
                    fg='#0000ff',
                    text=row['name'] + '/'),
                Button(
                    self.frame_dir,
                    text='View',
                    relief=RAISED,
                    command=lambda i=row['id']: self.update_directory(i))])
            # Add the Label to the row specified by 'start', column 0
            self.directory_contents[-1][0].grid(
                row=start, column=0, sticky=N + E + S + W)
            # Add the Button to the row specified by 'start', column 1
            self.directory_contents[-1][1].grid(
                row=start, column=1, sticky=N + E + S + W)
            # Increment 'start'.
            start += 1

        for row in self.directory_doc:
            # Each entry of the directory_contents list will be the entire row
            # of the grid. Each row is composed of a Label for that document
            # and a Button see the information about the document.
            self.directory_contents.append([
                Label(
                    self.frame_dir,
                    fg='#3399FF',
                    text=row['name']),
                Button(self.frame_dir,
                    text='Info',
                    relief=RAISED,
                    command=lambda i=row['id']: self.open_document(i))])
            # Add the Label to the row specified by 'start', column 0
            self.directory_contents[-1][0].grid(
                row=start, column=0, sticky=N + E + S + W)
            # Add the Button to the row specified by 'start', column 1
            self.directory_contents[-1][1].grid(
                row=start, column=1, sticky=N + E + S + W)
            # Increment 'start'.
            start += 1

        # Get the logical path for the supplied directory.
        path_logical = self.user.manage.manage_Dirs.get_directory_path(
            self.directory['id'])[0]
        # Set the Label to create a directory at the logical path.
        self.frame_create_banner_dir.config(
            text='Directory @ ' + path_logical + ':')
        # Set the Label to create a document at the logical path.
        self.frame_create_banner_doc.config(
            text='Document @ ' + path_logical + ':')
        return

    def open_document(self, docid):
        self.frame.grid_remove()
        self.editor_frame = Frame(self.master, self.frame)
        #self.editor_windows = DocUI(self.editor_frame)
        self.editor_windows = TextBox(self.master, self.editor_frame)
        self.editor_windows.initialize(self.user, Document(docid))
        self.editor_windows.frame.grid(row=0, column=0, sticky=N+E+S+W)

        self.buttons_frame = Frame(self.master, self.editor_frame)
        self.buttons_frame.grid(row=0, column=1, sticky=N)
        self.buttons_windows = DocSideButtons(self.buttons_frame, self.editor_windows, self.user)
        self.buttons_windows.grid(row=0, column=0, sticky=N+E+S+W)

        self.search_frame = Frame(self.master, self.editor_frame)
        self.search_frame.grid(row=1, column=0, sticky=W+E)
        self.search_UI = DocSearchUI(self.master, self.search_frame, self.editor_windows, self.status)
        #self.search_UI.grid(row=0, column=0, sticky=W+E)

        self.search_box_f = Frame(self.master, self.editor_frame)
        self.search_box_f.grid(row=2, column=0, sticky=W+E)
        self.box_UI = DocSearchBox(self.master, self.search_box_f)
        #self.box_UI.grid(row=0, column=0, sticky=W+E)

        self.menubar.destroy()
        self.init_menus()

        return

    def handler_directory_up(self):
        # If the current directory has a parent_dir:
        if self.directory['parent_dir']:
            # Update the Label to show the contents of parent_dir.
            self.update_directory(self.directory['parent_dir'])
        return

    def handler_create_directory(self):
        # The user is of the 'Regular Users' or 'Super User' usergroup.
        if self.user.info['usergroup'] <= 2:
            # Get the name of the directory the user wants to create.
            name = self.entry_dirname.get()
            # Create a new directory.
            res = self.user.create_new_directory(name, self.directory['id'])

            # If the directory was created:
            if res:
                # Delete the directory name from the creation box.
                self.entry_dirname.delete(0, len(name))
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
            name = self.entry_docname.get()
            # Create a document at the current directory.
            res = self.user.create_new_document(name, self.directory['id'])

            # If the document was created:
            if res:
                # Delete the document name from the creation box.
                self.entry_docname.delete(0, len(name))
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

    def handler_view_applications(self):
        self.frame.grid_remove()
        self.window_applications.frame.grid()

    def handler_view_complaints(self):
        self.frame.grid_remove()
        self.complaint_applications.frame.grid()

    def show_help(self):
        pass

    def show_about(self):
        pass

    def handler_view_invitations(self):
        self.window_invitations.frame.grid()
        return

    def handler_view_login(self):
        # Add the login frame to the bottom of the main window.
        self.window_login.frame.grid()
        return

    def handler_view_register(self):
        # Add the register frame to the bottom of the main window.
        self.register_window.frame.grid()

    def handler_view_logout(self):
        # Reset the user to the Guest user.
        self.user = Guest()

        # Re-initialize the control panel.
        self.init_frame_cpanel()
        # Add the control panel back to the grid.
        self.frame_cpanel.grid(
            row=0, column=1, rowspan=2, sticky=N + E + S + W,
            padx="20px", pady="10px")
        self.master.wm_geometry("")

        # Re-initialize the menus.
        self.init_menus()

    def handler_view_my_doc(self):
        self.frame.grid_remove()
        pass

    def handler_exit(self):
        self.frame.quit()
        return

if __name__ == "__main__":
    root = Tk()
    user = User(2)
    tb = Homepage(root, user)
    tb.frame.pack(fill='both', expand=1)
    mainloop()
