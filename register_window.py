from Tkinter import *
from sqlite3 import connect
from user import User, RegularUser, Guest
from md5 import new
import tkMessageBox
from manage import DBManager

class Register_Window:
    BASE_DIR = 'dbs'

    def __init__(self, master, parent, user):
        self.user = user
        self.parent = parent
        self.frame = Frame(master, relief=FLAT)
        self.manage_DB = DBManager()
        self.parent.frame.grid_remove()
        self.parent.frame.grid()
        self.init_register()
        self.frame_register.grid()

        return

    def init_register(self):
        self.frame_register = Frame(self.frame)

        self.username = StringVar()
        self.label_username = Label(self.frame_register, text="Username:")
        self.label_username.grid(row=0, column=0)
        self.entry_username = Entry(
            self.frame_register,
            textvariable=self.username)
        self.entry_username.grid(row=0, column=1)

        self.password_1 = StringVar()
        self.password_2 = StringVar()

        self.label_password = Label(self.frame_register, text="Password:")
        self.label_password.grid(row=1, column=0)
        self.entry_password_1 = Entry(
            self.frame_register,
            textvariable=self.password_1,
            show="*")
        self.entry_password_1.grid(row=1, column=1)

        self.label_password_2 = Label(self.frame_register, text='Confirm Password:')
        self.label_password_2.grid(row=2, column=0)
        self.entry_password_2 = Entry(
            self.frame_register,
            textvariable=self.password_2,
            show='*')
        self.entry_password_2.grid(row=2, column=1)
        #self.entry_password.bind("<KeyPress-Return>", self.user_login)

        self.email = StringVar()
        self.label_email = Label(self.frame_register, text="Email:")
        self.label_email.grid(row=3, column=0)
        self.entry_email = Entry(self.frame_register, textvariable=self.email)
        self.entry_email.grid(row=3, column=1)

        self.content = StringVar()
        self.label_content = Label(self.frame_register, text='Comments:')
        self.label_content.grid(row=4, column=0)
        self.entry_content = Entry(self.frame_register, textvariable=self.content)
        self.entry_content.grid(row=4, column=1)

        self.button_submit = Button(
            self.frame_register,
            text="Submit",
            command=self.handler_user_register)
        self.button_submit.grid(row=5, columnspan=2, sticky=W+E)
        self.frame_register.grid(row=0)

        return

    def handler_goto_homepage(self):
        self.frame.grid_remove()
        self.parent.frame.grid()
        self.parent.menubar.destroy()
        self.parent.init_menus()
        return

    def handler_user_register(self):
        username = self.username.get()
        password_1 = self.entry_password_1.get()
        password_2 = self.entry_password_2.get()
        email = self.email.get()
        content = self.content.get()
        user_exist = self.manage_DB.get_info('user', where={
                'username': username})
        if username and email and password_1 and password_2 \
           and content and not user_exist:
             if password_1 == password_2:
                 res = Guest().register(username, password_1, email, content)
                 tkMessageBox.showinfo('Successful', "You have just signed up an account. Please wait for system admin to approve your application. Thank you.")
                 return self.handler_goto_homepage()

             else:
                 tkMessageBox.showerror('Password do not match', 'The passwords you entered do not match. Try again!')
             return False
        elif user_exist:
             tkMessageBox.showerror('Failed', 'Username already taken. Please another one.')
             return False
        else:
             tkMessageBox.showerror('Failed', 'Please enter all the information correctly.')
             return False
