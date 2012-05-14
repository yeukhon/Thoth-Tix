from Tkinter import *
from user import User


class Invitation_Viewer_Window:
    BASE_DIR = 'dbs'

    def __init__(self, master, parent, user):
        self.user = user
        self.parent = parent

        self.frame = Frame(master, relief=FLAT)

        self.init_frame_pending()
        self.frame_pending.grid()

        self.init_frame_sent()
        self.frame_sent.grid(sticky=N + E + S + W)

        self.frame_quit = Button(
            self.frame,
            text='Home',
            command=self.handler_goto_homepage)
        self.frame_quit.grid()

        return

    def init_frame_pending(self):
        self.frame_pending = LabelFrame(
            self.frame,
            text='Pending Invitations')
        self.frame_pending.columnconfigure(0, weight=2)
        self.frame_pending.columnconfigure(1, weight=2)
        self.frame_pending.columnconfigure(2, weight=22)
        self.frame_pending.columnconfigure(3, weight=2)
        self.frame_pending.columnconfigure(4, weight=1)
        self.frame_pending.columnconfigure(5, weight=1)

        self.frame_pending_header_docid = Label(
            self.frame_pending,
            text='Document')
        self.frame_pending_header_docid.grid(row=0, column=0)

        self.frame_pending_header_from = Label(
            self.frame_pending,
            text='From')
        self.frame_pending_header_from.grid(row=0, column=1)

        self.frame_pending_header_message = Label(
            self.frame_pending,
            text='Message')
        self.frame_pending_header_message.grid(row=0, column=2)

        self.frame_pending_header_time = Label(
            self.frame_pending,
            text='Time')
        self.frame_pending_header_time.grid(row=0, column=3)

        self.frame_pending_header_action = Label(
            self.frame_pending,
            text='Action')
        self.frame_pending_header_action.grid(row=0, column=4, columnspan=2)

        res = self.user.manage.manage_User.get_invitations_to(self.user.info['id'])
        start = 1
        self.pending_invitations = []
        for row in res:
            self.pending_invitations.append([
                Label(
                    self.frame_pending,
                    text=row['docid']
                ),
                Label(
                    self.frame_pending,
                    text=row['userid_from']
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
                    text='Accept'
                ),
                Button(
                    self.frame_pending,
                    text='Deny'
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

    def init_frame_sent(self):
        self.frame_sent = LabelFrame(
            self.frame,
            text='Sent Invitations')
        self.frame_sent.columnconfigure(0)

        self.frame_sent_header_docid = Label(
            self.frame_sent,
            text='Document')
        self.frame_sent_header_docid.grid(row=0, column=0)

        self.frame_sent_header_from = Label(
            self.frame_sent,
            text='From')
        self.frame_sent_header_from.grid(row=0, column=1)

        self.frame_sent_header_message = Label(
            self.frame_sent,
            text='Message')
        self.frame_sent_header_message.grid(row=0, column=2)

        self.frame_sent_header_time = Label(
            self.frame_sent,
            text='Time')
        self.frame_sent_header_time.grid(row=0, column=3)

        self.frame_sent_header_action = Label(
            self.frame_sent,
            text='Status')
        self.frame_sent_header_action.grid(row=0, column=4)

        res = self.user.manage.manage_User.get_invitations_from(self.user.info['id'])
        start = 1
        self.sent_invitations = []
        for row in res:
            self.sent_invitations.append([
                Label(
                    self.frame_sent,
                    text=row['docid']
                ),
                Label(
                    self.frame_sent,
                    text=row['userid_to']
                ),
                Label(
                    self.frame_sent,
                    text=row['content']
                ),
                Label(
                    self.frame_sent,
                    text=row['time']
                ),
                Label(
                    self.frame_sent,
                    text=row['status']
                )
            ])
            self.sent_invitations[-1][0].grid(row=start, column=0)
            self.sent_invitations[-1][1].grid(row=start, column=1)
            self.sent_invitations[-1][2].grid(row=start, column=2)
            self.sent_invitations[-1][3].grid(row=start, column=3)
            self.sent_invitations[-1][4].grid(row=start, column=4)
            start += 1

        return

    def handler_goto_homepage(self):
        self.frame.grid_remove()
        self.parent.frame.grid()
        return

if __name__ == "__main__":
    root = Tk()
    user = User(2)
    tb = Invitation_Viewer_Window(root, 0, user)
    tb.frame.pack(fill='both', expand=1)
    mainloop()
