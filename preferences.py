import os
import json


class Preferences:
    BASE_DIR = "dbs"
    filename = '.preferences'

    def __init__(self):
        # Load the contents of the preferences file.
        self.load()
        return

    def load(self):
        # If the preferences file exist:
        if os.path.exists('%s/%s' % (self.BASE_DIR, self.filename)):
            # Create a handle to the preference file.
            fhandle = open('%s/%s' % (self.BASE_DIR, self.filename), 'r')

            # Initialize the info variable to the contents of the file.
            self.info = json.loads(fhandle.read())

            # Close the file.
            fhandle.close()
        # Else the preferences file does not exist:
        else:
            # Create a handle to the preference file.
            fhandle = open('%s/%s' % (self.BASE_DIR, self.filename), 'w')

            # Initialize the info variable to the defaults.
            self.info = {
                'line_numbers': False,
                'bg_color': '#FFFFFF',
                'fg_color': '#4D4D4D',
                'select_bg': '#339FFF',
                'select_fg': '#FFFFFF',
                'font_family': "Helvetica",
                'font_height': 12}

            # Write the contents of the info variable to the file.
            fhandle.write(json.dumps(self.info))

            # Close the file.
            fhandle.close()
        return

    def save(self):
         # Create a handle to the preference file.
        fhandle = open('%s/%s' % (self.BASE_DIR, self.filename), 'w')

        # Write the contents of the info variable to the file.
        fhandle.write(json.dumps(self.info))

        # Close the file.
        fhandle.close()
        return


if __name__ == "__main__":
    p = Preferences()
    print p.info
