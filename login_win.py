from Tkinter import *
from sqlite3 import connect
from user import User, RegularUser, SuperUser
from md5 import new
import tkMessageBox


class Login_Window:
    BASE_DIR = 'dbs'

    def __init__(self, master, parent, user):
        self.user = user
        self.parent = parent
        self.master = master
        self.frame = Frame(master, relief=FLAT)

        self.init_login()
        self.frame_login.grid()

        return

    def init_login(self):
        self.frame_login = Frame(self.frame)

        self.username = StringVar()
        self.label_username = Label(self.frame_login, text="Username:")
        self.label_username.grid(row=0, column=0)
        self.entry_username = Entry(
            self.frame_login,
            textvariable=self.username)
        self.entry_username.grid(row=0, column=1)

        self.password = StringVar()
        self.label_password = Label(self.frame_login, text="Password:")
        self.label_password.grid(row=1, column=0)
        self.entry_password = Entry(
            self.frame_login,
            textvariable=self.password,
            show="*")
        self.entry_password.grid(row=1, column=1)

        self.entry_password.bind("<KeyPress-Return>", self.user_login)

        self.button_login = Button(
            self.frame_login,
            text="Login",
            command=self.user_login)
        self.button_login.grid(row=2, columnspan=2, sticky=W+E)

        self.frame_login.grid(row=0)
        return

    def user_login(self, event=0):
        # Get the username the user typed.
        name = self.username.get()
        # Get the password the user typed and md5 it.
        password = self.password.get()

        # Check for the user in the database.
        res = self.user.login(name, password)

        # If the supplied user is in the database:
        if res:
            res = res[-1]
            if res['usergroup'] == 1:
                # Update the User instance with the new user information.
                self.parent.user = SuperUser(userid=res['id'])
            else:
                # Update the User instance with the new user information.
                self.parent.user = RegularUser(userid=res['id'])

            # Reset the username and password field.
            self.username.set('')
            self.password.set('')
            tkMessageBox.showinfo(
                'Authenticated', 'Welcome back! Logged in as %s' %res['username'])

            # Display the homepage.
            self.handler_goto_homepage()
        # The supplied username is not in the database.
        else:
            # Reset the username and password field.
            self.username.set('')
            self.password.set('')
        return

    def handler_goto_homepage(self):
        # Remove the login frame from the window.
        self.frame.grid_remove()

        # Re-initialize the Control Panel.
        self.parent.init_frame_cpanel()

        # Added the Control Panel to the parent frame.
        self.parent.frame_cpanel.grid(
            row=0, column=1, rowspan=2, sticky=N + E + S + W,
            padx="20px", pady="10px")

        # Add the parent frame to the main frame.
        self.parent.frame.grid()
        self.master.wm_geometry("")

        self.parent.menubar.destroy()
        self.parent.init_menus()
        return
