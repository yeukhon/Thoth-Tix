#  user.py
#
#  Copyright 2012 Kevin Ramdath <KRPent@gmail.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#
from manage import Manager, AdminManager
from md5 import new
from datetime import datetime
import time


class User(object):

    def __init__(self, userid=0, username=''):
        # Initialize an instance of the Manager class for this user.
        self.manage = Manager()

        # Retrive the information for the current user based on the supplied
        # userid or username.
        self.update_user(userid=userid, username=username)

        return

    def update_user(self, userid=0, username=''):
        # If the userid was supplied:
        if userid:
            # Search for the user information by userid.
            res = self.manage.manage_DB.get_info('user', rowid=userid)
            # If the userid was found in the database:
            if res:
                # Set the information of the current user as the result.
                self.info = res
            # Else the userid was not found in the database.
            else:
                # Get the information for the guest user.
                self.info = self.manage.manage_DB.get_info('user', rowid=1)
        # Else if the username was supplied:
        elif username:
            # Search for the user information by username.
            res = self.manage.manage_DB.get_info('user', where={
                'username': username})
            # If the userid was found in the database:
            if res:
                # Set the information of the current user as the result.
                self.info = res[0]
            # Else the userid was not found in the database.
            else:
                # Get the information for the guest user.
                self.info = self.manage.manage_DB.get_info('user', rowid=1)
        # Else neither the userid nor the username was supplied:
        else:
            # Default user, Guest.
            self.info = self.manage.manage_DB.get_info('user', rowid=1)

        # Set the information of the current user for the manager to be the
        # information that was just found.
        self.manage.manage_DB.update_user_info(self.info)
        return

    def comment(self, docid, content, verbose=False):
        # Insert the supplied information into the database.
        res = self.manage.manage_DB.insert_info('comment', insert={
            'docid': docid,
            'userid': self.info['id'],
            'content': content,
            'time': time.time()}, verbose=verbose)

        # If the insertion was successful:
        if res:
            # Return True to denote success.
            return True
        # Else the insertion was unsuccessful:
        else:
            # Return False to denote failure.
            return False

    def complain(self, docid, content, verbose=False):
        # Insert the supplied information into the database.
        res = self.manage.manage_DB.insert_info('complaint', insert={
            'docid': docid,
            'userid': self.info['id'],
            'content': content,
            'time': time.time(),
            'response': ''}, verbose=verbose)

        # If the insertion was successful:
        if res:
            # Return True to denote success.
            return True
        # Else the insertion was unsuccessful:
        else:
            # Return False to denote failure.
            return False


class Guest(User):

    def __init__(self):
        # Initialize the user information and the Manager instance based on
        # the parent class, User.
        super(Guest, self).__init__(userid=1)
        return

    def register(self, username, password, email, content, verbose=False):
        # Insert the supplied information into the database.
        res = self.manage.manage_DB.insert_info('application', insert={
            'username': username,
            'password': new(password).hexdigest(),
            'email': email,
            'content': content,
            'time': time.time()}, verbose=verbose)

        # If the insertion was successful:
        if res:
            # Return True to denote success.
            return True
        # Else the insertion was unsuccessful:
        else:
            # Return False to denote failure.
            return False

    def login(self, username, password, verbose=False):
        # Get the supplied user information from the database.
        res = self.manage.manage_DB.get_info('user', where={
            'username': username,
            'password': new(password).hexdigest()}, verbose=verbose)

        # If the user was found:
        if res:
            # Return True to denote success.
            return res
        # Else the user was not found:
        else:
            # Return {} to denote failure.
            return {}


class RegularUser(User):

    def __init__(self, userid=0, username=''):
        # Initialize the user information and the Manager instance based on
        # the parent class, User.
        super(RegularUser, self).__init__(userid=userid, username=username)
        return

    def create_new_document(self, name, parent_dir, verbose=False):
        # Insert a document with the supplied information into the database.
        res = self.manage.manage_DB.insert_info('document', insert={
            'name': name,
            'parent_dir': parent_dir,
            'owner': self.info['id']}, verbose=verbose)

        #If the insertion operation was successful:
        if res:
            # Get the docid for the inserted document.
            res = self.manage.manage_DB.get_info('document', where={
                'name': name,
                'parent_dir': parent_dir,
                'owner': self.info['id']}, verbose=verbose)
            docid = res[0]['id']

            # Create the document in the supplied folder.
            res = self.manage.manage_Docs.create_document(docid, parent_dir)

            # If the document was created successfully:
            if res:
                # Return True to indicate success.
                return True

        # Return False to indicate failure.
        return False

    def create_new_directory(self, name, parent_dir, verbose=False):
        # Insert a directory with the supplied information into the database.
        res = self.manage.manage_DB.insert_info('directory', insert={
            'name': name,
            'parent_dir': parent_dir}, verbose=verbose)

        res = self.manage.manage_DB.get_info('directory', where={
            'name': name,
            'parent_dir': parent_dir}, verbose=verbose)

        #If the insertion operation was successful:
        if res:
            # Get the dirid for the inserted directory.
            res = self.manage.manage_DB.get_info('directory', where={
                'name': name,
                'parent_dir': parent_dir}, verbose=verbose)
            dirid = res[0]['id']

            # Create the directory in the supplied folder.
            res = self.manage.manage_Dirs.create_directory(dirid)

            # If the document was created successfully:
            if res:
                # Return True to indicate success.
                return True

        # Return False to indicate failure.
        return False

    def send_invitation_to(self, docid, userid_to, content, verbose=False):
        # Insert in invitation with the supplied information.
        res = self.manage.manage_DB.insert_info('invitation', insert={
            'docid': docid,
            'userid_from': self.info['id'],
            'userid_to': userid_to,
            'content': content,
            'time': time.time()}, verbose=verbose)

        # If the insertion was successful:
        if res:
            # Return True to denote success.
            return True
        # Else the insertion was unsuccessful:
        else:
            # Return False to denote failure.
            return False


class SuperUser(User):

    def __init__(self, userid=0, username=''):
        # Initialize the user information and the Manager instance based on
        # the parent class, User.
        super(SuperUser, self).__init__(userid=userid, username=username)

        # Initialize the manger for the admin.
        self.manage.manage_Admin = AdminManager(self.manage.manage_DB)
        return

    def accept_application(self, appid, verbose=False):
        # Set the status of the application with the supplied appid to be
        # 'Accepted'.
        res = self.manage.manage_DB.update_info('application',
            update={'status': 1}, where={'id': appid}, verbose=verbose)

        # If the update operation was performed successfully:
        if res:
            # Get the information for the supplied application.
            res = self.manage.manage_DB.get_info('application', rowid=appid,
                verbose=verbose)
            username = res['username']

            # Add a user with the information supplied in the current
            # application.
            res = self.manage.manage_DB.insert_info('user', insert={
                'username': username,
                'password': res['password'],
                'email': res['email'],
                'usergroup': res['usergroup']}, verbose=verbose)

            # If the insertion operation was performed successfully:
            if res:
                # Create the user dictionary for the new user.
                self.manage.manage_DB.init_table_usrdic(username=username)

                # Return True to indicate success.
                return True

        # Return False to indicate failure.
        return False

    def deny_application(self, appid, verbose=False):
        # Set the status of the application with the supplied appid to be
        # 'Denied'.
        res = self.manage.manage_DB.update_info('application',
            update={'status': -1}, where={'id': appid}, verbose=verbose)

        # If the update operation was performed successfully:
        if res:
            # Return True to indicate success.
            return True

        # Return False to indicate failure.
        return False

    def get_all_complaints(self):
        # Query for all complaints for the supplied document.
        rows = self.manage.manage_DB.get_info('complaint', where={
            'status':0})

        # Return comments as a list.
        res = []
        for row in rows:
            # Get the information for the supplied document.
            doc_info = self.manage.manage_DB.get_info('document',
                rowid=row['docid'])

            # Get the information for the user that wrote the comment.
            usr_info = self.manage.manage_DB.get_info('user',
                rowid=row['userid'])

            # Create a dictionary with the results and add the dictionary to
            # the list.
            res.append({'id': row['id'], 'doc': doc_info['name'],
                'user': usr_info['username'], 'content': row['content'],
                'time': datetime.fromtimestamp(int(row['time']))})

        # Return the list of results.
        return res

    def response_complaint(self, compid, valid, response, verbose=False):
        if verbose: print '\nStarting response_complaint:'

        # If valid is -1 (invalid) or 1 (valid):
        if valid == -1 or valid == 1:
            # Set the response field of the supplied complaint to be the
            # supplied response and status.
            res = self.manage.manage_DB.update_info('complaint', update={
                'status': valid, 'response': response}, where={'id': compid},
                verbose=verbose)

            # If the update operation was performed successfully:
            if res:
                # If the complaint was valid:
                if valid == 1:
                    # Get the information for the supplied complaint.
                    res = self.manage.manage_DB.get_info('complaint',
                        rowid=compid, verbose=verbose)
                    docid = res['docid']

                    # Get the information for the document the complaint was
                    # issued upon.
                    res = self.manage.manage_DB.get_info('document',
                        rowid=docid, verbose=verbose)
                    infraction = res['infraction'] + 1
                    owner = res['owner']

                    # Increment the infraction number for the document.
                    res = self.manage.manage_DB.update_info('document',
                        update={'infraction': infraction}, where={
                        'id': docid}, verbose=verbose)

                    # If infraction is equal to 4:
                    if infraction == 4:
                        # This document is suspended, so get the information
                        # for the owner.
                        res = self.manage.manage_DB.get_info('user',
                            rowid=owner, verbose=verbose)
                        infraction = res['infraction'] + 1

                        # Increment the infraction number of the owner.
                        res = self.manage.manage_DB.update_info('user',
                            update={'infraction': infraction}, where={
                            'id': owner}, verbose=verbose)

                        # If infraction is equal to 3:
                        if infraction == 3:
                            # This user should be banned, so get the id for the
                            # banned usergroup.
                            res = self.manage.manage_DB.get_info('usergroup',
                                where={'name': 'Suspended'}, verbose=verbose)
                            group = res[0]['id']

                            # Update the owner to be part of the Suspended
                            # usergroup.
                            res = self.manage.manage_DB.update_info('user',
                                update={'usergroup': group}, where={
                                'id': owner}, verbose=verbose)

                    # Return True to indicate success.
                    return True
                # Else the complaint was invalid:
                else:
                    # Return True to indicate success.
                    return True

        # Return False to denote failure.
        return False

if __name__ == "__main__":
    # Each test is independent of the others.
    verbose = False
    gu = Guest()
    ru = RegularUser(3)
    su = SuperUser(2)

    ###########################################################################
    # TU1 = Testing create new document
    ###########################################################################
    res = ru.create_new_document('TU1.txt', 1, verbose=verbose)
    print 'Create New Document:', res
    res = ru.manage.manage_DB.get_info('document', where={
        'name': 'TU1.txt', 'parent_dir': 1}, verbose=verbose)
    print 'Document in dB:', True if res else False

    ###########################################################################
    # TU2 = Testing comment
    ###########################################################################
    # Create a document to comment about as the RegularUser.
    ru.create_new_document('TU2.txt', 1, verbose=verbose)
    # Get the id of the inserted document.
    docid = gu.manage.manage_DB.get_info('document', where={
        'name': 'TU2.txt', 'parent_dir': 1, 'owner': ru.info['id']},
        verbose=verbose)[0]['id']
    # Comment on the document.
    res = gu.comment(docid, "TU2 comment", verbose=verbose)
    print 'Comment as Guest:', res

    ###########################################################################
    # TU3 = Testing complain
    ###########################################################################
    # Create a document to complain about as the RegularUser.
    ru.create_new_document('TU3.txt', 1, verbose=verbose)
    # Get the id of the inserted document.
    docid = gu.manage.manage_DB.get_info('document', where={
        'name': 'TU3.txt', 'parent_dir': 1, 'owner': ru.info['id']},
        verbose=verbose)[0]['id']
    # Comment on the document.
    res = gu.complain(docid, "TU3 complaint", verbose=verbose)
    print 'Complain as Guest:', res

    ###########################################################################
    # TU4 = Testing Register
    ###########################################################################
    res = gu.register('TU4', 'TU4', 'TU4@domain.com', 'TU4 register',
        verbose=verbose)
    print 'Registering as Guest:', res
    res = su.manage.manage_DB.get_info('application', where={
        'username': 'TU4', 'password': 'TU4', 'email': 'TU4@domain.com',
        'content': 'TU4 register'}, verbose=verbose)
    print 'Application in dB:', True if res else False

    ###########################################################################
    # TU5 = Testing Accept Application:
    ###########################################################################
    # Register as the Guest.
    gu.register('TU5', 'TU5', 'TU5@domain.com', 'TU5 register', verbose=verbose)
    # Get the id for the inserted application.
    appid = su.manage.manage_DB.get_info('application', where={
        'username': 'TU5', 'email': 'TU5@domain.com'},
        verbose=verbose)[0]['id']
    # Accept the application.
    res = su.accept_application(appid, verbose=verbose)
    print 'Accept Application as SuperUser:', res

    ###########################################################################
    # TU6 = Testing Deny Application:
    ###########################################################################
    # Register as the Guest.
    gu.register('TU6', 'TU6', 'TU6@domain.com', 'TU6 register', verbose=verbose)
    # Get the id for the inserted application.
    appid = su.manage.manage_DB.get_info('application', where={
        'username': 'TU6', 'email': 'TU6@domain.com'},
        verbose=verbose)[0]['id']
    # Deny the application.
    res = su.deny_application(appid, verbose=verbose)
    print 'Deny Application as SuperUser:', res

    ###########################################################################
    # TU7 = Testing Response to Valid Complaint:
    ###########################################################################
    # Create a document to complain about as the RegularUser.
    ru.create_new_document('TU7.txt', 1, verbose=verbose)
    # Get the id of the inserted document.
    docid = gu.manage.manage_DB.get_info('document', where={
        'name': 'TU7.txt', 'parent_dir': 1, 'owner': ru.info['id']},
        verbose=verbose)[0]['id']
    for i in range(5):
        # Insert Complaint as the Guest.
        gu.complain(docid, "TU7 complaint #%s" % i, verbose=verbose)
        # Get the id for the inserted complaint.
        compid = su.manage.manage_DB.get_info('complaint', where={
            'docid': docid, 'userid': gu.info['id'],
            'content': "TU7 complaint #%s" % i},
            verbose=verbose)[0]['id']

        # Respond to the complaint.
        res = su.response_complaint(compid, 1, 'TU7 response #%s' % i,
            verbose=verbose)
        print 'Response #%s Valid Complaint as SuperUser:' % i, res

    ###########################################################################
    # TU8 = Testing Response to Invalid Complaint:
    ###########################################################################
    # Create a document to complain about as the RegularUser.
    ru.create_new_document('TU8.txt', 1, verbose=verbose)
    # Get the id of the inserted document.
    docid = gu.manage.manage_DB.get_info('document', where={
        'name': 'TU8.txt', 'parent_dir': 1, 'owner': ru.info['id']},
        verbose=verbose)[0]['id']
    # Insert Complaint as the Guest.
    gu.complain(docid, "TU8 complaint", verbose=verbose)
    # Get the id for the inserted complaint.
    compid = su.manage.manage_DB.get_info('complaint', where={
        'docid': docid, 'userid': gu.info['id'], 'content': "TU8 complaint"},
        verbose=verbose)[0]['id']

    # Respond to the complaint.
    res = su.response_complaint(compid, -1, 'TU8 response', verbose=verbose)
    print 'Response 2 Invalid Complaint as SuperUser:', res

    ###########################################################################
    # TU9 = Testing create new directory
    ###########################################################################
    res = ru.create_new_directory('TU9', 1, verbose=verbose)
    print 'Create New Directory:', res
    res = ru.manage.manage_DB.get_info('directory', where={
        'name': 'TU9', 'parent_dir': 1}, verbose=verbose)
    print 'Directory in dB:', True if res else False

    ###########################################################################
    # TU10 = View Pending Application:
    ###########################################################################
    # Register as the Guest.
    gu.register('TU10', 'TU10', 'TU10@domain.com', 'TU10 register', verbose=verbose)
    # Get the id for the inserted application.
    appid = su.manage.manage_DB.get_info('application', where={
        'username': 'TU10', 'email': 'TU10@domain.com'},
        verbose=verbose)[0]['id']
    # Accept the application.
    res = su.manage.manage_Admin.get_pending_applications()
    print 'Pending Applications as SuperUser:', res

    print '\n'
    su.manage.manage_DB.print_DB('user')
    print '\n'
    su.manage.manage_DB.print_DB('document')
