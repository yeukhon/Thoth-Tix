class Menubar:

    def __init__(self, frame, user):
        self.frame = frame
        self.user = user

        return

    def init_file_menu(self):
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
            self.menubar.add_cascade(label="File", menu=self.loginmenu)
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

        self.top = master.winfo_toplevel()
        self.top["menu"] = self.menubar
