from Tkinter import *
from sqlite3 import connect
from user import User


class App_Viewer_Window:
    BASE_DIR = 'dbs'

    def __init__(self, master, parent, user):
        self.master = master
        self.user = user
        self.parent = parent

        self.frame = Frame(master, relief=FLAT)

        self.init_frame_pending()
        self.frame_pending.grid()

        return

    def init_frame_pending(self):
        self.frame_pending = LabelFrame(
            self.frame,
            text='Pending Applications')
        self.frame_pending.columnconfigure(0, weight=2)
        self.frame_pending.columnconfigure(1, weight=2)
        self.frame_pending.columnconfigure(2, weight=22)
        self.frame_pending.columnconfigure(3, weight=2)
        self.frame_pending.columnconfigure(4, weight=1)
        self.frame_pending.columnconfigure(5, weight=1)

        self.frame_pending_header_username = Label(
            self.frame_pending,
            text='Username')
        self.frame_pending_header_username.grid(row=0, column=0)

        self.frame_pending_header_email = Label(
            self.frame_pending,
            text='Email')
        self.frame_pending_header_email.grid(row=0, column=1)

        self.frame_pending_header_content = Label(
            self.frame_pending,
            text='Content')
        self.frame_pending_header_content.grid(row=0, column=2)

        self.frame_pending_header_time = Label(
            self.frame_pending,
            text='Time')
        self.frame_pending_header_time.grid(row=0, column=3)

        self.frame_pending_header_action = Label(
            self.frame_pending,
            text='Action')
        self.frame_pending_header_action.grid(row=0, column=4, columnspan=2)

        res = self.user.manage.manage_Admin.get_pending_applications()
        start = 1
        self.pending_invitations = []
        for row in res:
            self.pending_invitations.append([
                Label(
                    self.frame_pending,
                    text=row['username']
                ),
                Label(
                    self.frame_pending,
                    text=row['email']
                ),
                Label(
                    self.frame_pending,
                    text=row['content']
                ),
                Label(
                    self.frame_pending,
                    text=row['time']
                ),
                Button(
                    self.frame_pending,
                    text='Accept',
                    #command=self.handler_approve
                    command=lambda i=row['id']:self.handler_approve(i)
                ),
                Button(
                    self.frame_pending,
                    text='Deny',
                    command=lambda i=row['id']:self.handler_disapprove(i)
                )
            ])
            self.pending_invitations[-1][0].grid(row=start, column=0)
            self.pending_invitations[-1][1].grid(row=start, column=1)
            self.pending_invitations[-1][2].grid(row=start, column=2)
            self.pending_invitations[-1][3].grid(row=start, column=3)
            self.pending_invitations[-1][4].grid(row=start, column=4)
            self.pending_invitations[-1][5].grid(row=start, column=5)
            start += 1

        return

    def handler_goto_homepage(self):
        self.frame.grid_remove()
        self.parent.frame.grid_remove()
        self.parent.init_frame(self.master)
        self.parent.frame.grid()
        return

    def handler_approve(self, rowid):
        res = self.user.accept_application(rowid, verbose=True)
        if res:
            self.frame_pending.grid_remove()
            self.init_frame_pending()
            self.frame_pending.grid()
        else:
            tkMessageBox.showerror('Failed', 'Approval failed.')

    def handler_disapprove(self, rowid):
        res = self.user.deny_application(rowid, verbose=True)
        if res:
            self.frame_pending.grid_remove()
            self.init_frame_pending()
            self.frame_pending.grid()
        else:
            tkMessageBox.showerror('Failed', 'Denial failed.')

class App_Form_Window:
    BASE_DIR = 'dbs'

    def __init__(self, master, parent, user):
        self.user = user
        self.parent = parent

        self.frame = Frame(master, relief=FLAT)

        self.init_frame_form()
        self.frame_form.grid()

        self.frame_quit = Button(
            self.frame,
            text='Home',
            command=self.handler_goto_homepage)
        self.frame_quit.grid()

        return

    def init_frame_form(self):
        self.frame_form = LabelFrame(
            self.frame,
            text='Apply To The System')
        self.frame_form.columnconfigure(0, weight=2)
        self.frame_form.columnconfigure(1, weight=2)
        self.frame_form.columnconfigure(2, weight=22)
        self.frame_form.columnconfigure(3, weight=2)
        self.frame_form.columnconfigure(4, weight=1)
        self.frame_form.columnconfigure(5, weight=1)

        place = 0
        self.form_username = StringVar()
        self.frame_form_label_username = Label(
            self.frame_form,
            text='Username:')
        self.frame_form_label_username.grid(row=place, column=0)
        self.frame_form_username = Entry(
            self.frame_form,
            textvariable=self.form_username)
        self.frame_form_username.grid(row=place, column=1)

        place += 1
        self.form_password = StringVar()
        self.frame_form_label_password = Label(
            self.frame_form,
            text='Password:')
        self.frame_form_label_password.grid(row=place, column=0)
        self.frame_form_password = Entry(
            self.frame_form,
            textvariable=self.form_password,
            show='*')
        self.frame_form_password.grid(row=place, column=1)

        place += 1
        self.form_password2 = StringVar()
        self.frame_form_label_password2 = Label(
            self.frame_form,
            text='Confirm Password:')
        self.frame_form_label_password2.grid(row=place, column=0)
        self.frame_form_password2 = Entry(
            self.frame_form,
            textvariable=self.form_password2,
            show='*')
        self.frame_form_password2.grid(row=place, column=1)

        place += 1
        self.form_email = StringVar()
        self.frame_form_label_email = Label(
            self.frame_form,
            text='Email:')
        self.frame_form_label_email.grid(row=place, column=0)
        self.frame_form_email = Entry(
            self.frame_form,
            textvariable=self.form_email)
        self.frame_form_email.grid(row=place, column=1)

        place += 1
        self.form_content = StringVar()
        self.frame_form_label_content = Label(
            self.frame_form,
            text='Reason:')
        self.frame_form_label_content.grid(row=place, column=0)
        self.frame_form_content = Text(
            self.frame_form,
            height=5,
            width=23,
            wrap=WORD)
        self.frame_form_content.insert(
            END,
            'What is your pourpose in joining the system?')
        self.frame_form_content.grid(row=place, column=1)

        place += 1
        self.frame_form_submit = Button(
            self.frame_form,
            text='Submit',
            command=self.handler_submit_form)
        self.frame_form_submit.grid(row=place, columnspan=2)

        return

    def handler_submit_form(self):
        # Extract the username the user has typed.
        username = self.form_username.get()

        # Check whether the username is already in the database.
        res = self.user.manage.manage_DB.get_info('user', where={
            'username': username})

        # If the username is already in the database:
        if res:
            # Turn the username field to red.
            self.frame_form_username.config(bg='red')
            # Return false to indicate failure
            return False
        # Else the username is not in the database:
        else:
            # Turn the username field basck to normal.
            self.frame_form_username.config(bg='light gray')

        # If both password fields do not match:
        if self.form_password.get() != self.form_password2.get():
            # Turn both password fields to red.
            self.frame_form_password.config(bg='red')
            self.frame_form_password2.config(bg='red')
            # Return false to indicate failure
            return False
        # Else both password fields match:
        else:
            # Turn both password fields back to normal.
            self.frame_form_password.config(bg='light gray')
            self.frame_form_password2.config(bg='light gray')

        # Extract the password, email, and content the user has typed.
        password = self.form_password.get()
        email = self.form_email.get()
        content = self.form_content.get()
        # Insert the application into the database via the register method of
        # the guest user and return the result of the insertion.
        return self.user.register(username, password, email, content)

    def handler_goto_homepage(self):
        self.frame.grid_remove()
        self.parent.frame.grid()
        return


if __name__ == "__main__":
    root = Tk()
    user = User(2)
    tb = App_Viewer_Window(root, 0, user)
#    tb = App_Form_Window(root, 0, user)
    tb.frame.pack(fill='both', expand=1)
    mainloop()
