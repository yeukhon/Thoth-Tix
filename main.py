from Tkinter import *
from user import *
from textbox import *
from homepage import Homepage


class TEditor(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()

        self.master.title("TEditor")

        self.user = Guest()
        self.main_GUI = Homepage(master, self.user)
        self.main_GUI.frame.grid(row=0, column=0, sticky=N+E+S+W)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        return


if __name__ == "__main__":
    root = Tk()
    app = TEditor(root)
    root.wm_geometry("")
    root.mainloop()
