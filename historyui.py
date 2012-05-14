from textbox import TextBox
from datetime import datetime
import os
import json


class HistoryUI:

    def __init__(self, master, parent, document):
        self.parent = parent
        self.master = master
        self.document = document
        self.frame = Frame(master, relief=FLAT)

        # Get the history for the supplied document.
        self.get_document_history()

        # If there is a history for the supplied document:
        if self.history:
            # Create a variable to hold the history frames.
            self.frames = []
            # For 3 times:
            for item in self.history:
                # Append the history frame for the current history.
                self.frames.append(self.init_frame_history(item))
                self.frames[-1].grid()
        # Else there is no history for the supplied document:
        else:
            Label(self.frame, text="There are no changes to the document!").grid()

        self.frame.grid()

        return

    def get_document_history(self):
        # If the mod file for the supplied document exist:
        if os.path.exists('%s/M%s' % (self.document.info['ppath'],
            self.document.info['id'])):
            # Create a handle to the mod file.
            mhandle = open('%s/M%s' % (self.document.info['ppath'],
                self.document.info['id']), 'r')

            # Read the contents of the file and create a json object.
            self.history = json.loads(mhandle.read())

            # Close the file handle.
            mhandle.close()

            # Return True to indicate success.
            return True
        # Else there has been no modifications to the file:
        else:
            self.history = None

            # Return false to indicate failure.
            return False

    def init_frame_history(self, history):
        # Get the user who made the current changes.
        user = self.document.manage.manage_DB.get_info('user', where={
            'id': history['userid']})

        # If the user was not found:
        if not user:
            # User is default Anon.
            user = 'Anon'
        # Else user was found:
        else:
            user = user[0]['username']

        frame_history = LabelFrame(
            self.frame,
            text='By %s @ %s' % (user, datetime.fromtimestamp(int(history['time']))))

        height = len(history['content'])
        if height > 10:
            height = 10

        text_history = Text(frame_history, height=height)
        text_history.pack(side=LEFT, fill='both', expand=1)

        # The vertical scrollbar.
        scroll_vbar = Scrollbar(frame_history, orient=VERTICAL)
        scroll_vbar.pack(fill='y', side=RIGHT)

        # The vertical scrollbar needs to be linked to the text widget that has
        # the user content otherwise the scrollbar will not scroll the text.
        text_history.config(yscrollcommand=scroll_vbar.set)
        scroll_vbar.config(command=text_history.yview)

        text_history.insert('1.0', '\n'.join(history['content']))
        text_history.config(state=DISABLED)

        return frame_history


if __name__ == "__main__":
    from user import RegularUser
    from document import Document
    from Tkinter import *

    verbose = False
    ###########################################################################
    # TH0 = Setup
    ###########################################################################
    # Create an instance of the User class for the newly created user, when the
    # admin accepts an application, the user is automatically created.
    ash = RegularUser(username='Ash')
    # Create a document at the root directory.
    ash.create_new_document('TH0.txt', 1, verbose=verbose)
    # Get the 'id' of the newly created document.
    pikaid = ash.manage.manage_DB.get_info('document', where={
        'name': 'TH0.txt', 'parent_dir': 1}, verbose=verbose)[0]['id']
    # Create an instance of the User class for the newly created document.
    pikachu = Document(pikaid)
    # Save new content to the document.
    pikachu.save("Good Morning!\nGood Morning to you!\nHow do you do?\nFine thank you, yourself?\nI am well.\nGoodbye.\nGoodbye.", ash.info['id'], verbose=verbose)

    # Save new content to the document.
    pikachu.save("Good Morning!\nHow do you do?\nI am well.\nGoodbye.", ash.info['id'], verbose=verbose)

    ###########################################################################
    # TH1 = Revision
    ###########################################################################
    # Create the GUI.
    root = Tk()
    hui = HistoryUI(root, root, pikachu)
    mainloop()
