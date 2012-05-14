from textbox import TextBox
from datetime import datetime
import os
import json
import Tix


class HistoryUI(Tix.Frame):

    def __init__(self, master, document):
        self.master = master
        self.document = document
        self.frame = Tix.Frame(master)

        print 'pass frame'
        # Get the history for the supplied document.
        self.get_document_history()
        print 'pass gdh'
        # Create a variable to hold the history frames.
        self.frames = []
        # If there is a history for the supplied document:
        if self.history:
            print 'pass doc his'
            # For 3 times:
            for item in self.history:
                if item['content']:
                    print item
                    # Append the history frame for the current history.
                    self.frames.append(self.init_frame_history(item))
                    self.frames[-1].pack(side=Tix.TOP, padx=2, pady=2,
                        fill=Tix.BOTH, expand=1)
        # Else there is no history for the supplied document:
        if len(self.frames) == 0:
            lb = Tix.Label(self.frame,
                text="There are no changes to the document!")
            lb.pack(side=Tix.TOP, padx=2, pady=2, fill=Tix.BOTH, expand=1)



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
        print 'pass user'
        # If the user was not found:
        if not user:
            # User is default Anon.
            user = 'Anon'
        # Else user was found:
        else:
            user = user[0]['username']
        print 'pass name', user
        frame_history = Tix.ScrolledHList(self.frame)
        frame_history.pack(side=Tix.TOP, padx=20, pady=2, fill=Tix.BOTH, expand=1)
        print 'pass shl'
        frame_history.hlist.add('user', itemtype=Tix.TEXT,
            text='By %s @ %s' % (user,
            datetime.fromtimestamp(int(history['time']))))

        #~ height = len(history['content'])
        #~ if height > 10:
            #~ height = 10

        count = 0
        for i in history['content']:
            frame_history.hlist.add('H%s' % count, itemtype=Tix.TEXT,
                text=i)
            count += 1

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
