#  manage.py
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
from database import Database
from porter import PorterStemmer
from datetime import datetime
import os
import re
import time


class Manager(object):

    def __init__(self):
        # Intitialize the manager class.
        self.manage_DB = DBManager()

        # Initialize the manager for the users.
        self.manage_User = UserManager(self.manage_DB)
        # Initialize the manager for the documents.
        # Initialize the manager for the directories.
        self.manage_Docs = DocumentManager(self.manage_DB)
        self.manage_Dirs = DirectoryManager()
        # Initialize the manager for the index.
        self.manage_Indx = IndexManager(self.manage_DB)

        return


class DBManager(Database):

    def __init__(self, user_info={}):
        # Call the constuctor of the Database class.
        super(DBManager, self).__init__()

        # If the user information was supplied:
        if user_info:
            # Set the current user information to the supplied user.
            self.user_info = user_info
        # Else the user information was not supplied:
        else:
            # Initialize the current user information to be the guest user.
            self.user_info = super(DBManager, self)._get_info('user', rowid=1)
        return

    def update_user_info(self, info):
        # Set the current user information to the supplier information.
        self.user_info = info
        return

    def insert_info(self, table, insert={}, verbose=False):
        # If the user has permission to preform the supplied action:
        if self.check_rights(table, 'INSERT'):
            return super(DBManager, self)._insert_info(
                table, insert=insert, verbose=verbose)
        # Else the user does not have persmission to preform the supplied action.
        else:
            # Return False to indicate fauilure.
            return False

    def get_info(self, table, rowid=0, where={}, verbose=False):
        # If the user has permission to preform the supplied action:
        if self.check_rights(table, 'GET'):
            return super(DBManager, self)._get_info(
                table, rowid=rowid, where=where, verbose=verbose)
        # Else the user does not have persmission to preform the supplied action.
        else:
            # Return False to indicate fauilure.
            return False

    def update_info(self, table, update={}, where={}, verbose=False):
        # If the user has permission to preform the supplied action:
        if self.check_rights(table, 'GET'):
            return super(DBManager, self)._update_info(
                table, update=update, where=where, verbose=verbose)
        # Else the user does not have persmission to preform the supplied action.
        else:
            # Return False to indicate fauilure.
            return False

    def check_rights(self, table, action):
        # Check whether the current user has permission to preform the supplied
        # action on the supplied table.

        # If the user wants to access the user dictionary table:
        if table[0] == 'X':
            # Return True.
            return True

        #~ 0 --- no permission
        #~ 1 --g get
        #~ 2 -u- update
        #~ 3 -ug update and get
        #~ 4 i-- insert
        #~ 5 i-g insert and get
        #~ 6 iu- insert and update
        #~ 7 iug insert, update and get

        # Get the permissions for the current user's usergroup.
        res = super(DBManager, self)._get_info('usergroup',
            rowid=self.user_info['usergroup'])

        # If there are any permissions:
        if res:
            # Get the permission for the supplied table.
            permission = res[table]

            # If the permission is 0:
            if not permission:
                # Return False to indicated that the user does not have
                # permission to preform the supplied action.
                return False
            # Else if the current user wants to GET information from the
            # supplied table.
            elif action == 'GET':
                # If the permission field has the GET flag:
                if permission & 1 == 1:
                    # Return True to indicated that the user has permission to
                    # preform the supplied action.
                    return True
            # Else if the current user wants to UPDATE information in the
            # supplied table.
            elif action == 'UPDATE':
                # If the permission field has the UPDATE flag:
                if permission & 2 == 2:
                    # Return True to indicated that the user has permission to
                    # preform the supplied action.
                    return True
            # Else if the current user wants to INSERT information into the
            # supplied table.
            elif action == 'INSERT':
                # If the permission field has the INSERT flag:
                if permission & 4 == 4:
                    # Return True to indicated that the user has permission to
                    # preform the supplied action.
                    return True

        # Return False to indicated that the user does not have permission to
        # preform the supplied action.
        return False


class UserManager:

    def __init__(self, dbm):
        # Save a instance of the supplied Manager class for later user.
        self.manage_DB = dbm
        return

    def get_invitations_to(self, userid):
        # Get the information for the supplied user.
        usr_to = self.manage_DB.get_info('user', rowid=userid)

        # If the supplied user is not a 'Visitor':
        if usr_to['usergroup'] != 4:
            # Query for all invitations to the supplied user.
            rows = self.manage_DB.get_info('invitation', where={
                'userid_to': userid, 'status':0})

            # Initialize the list that will hold the results.
            res = []
            for row in rows:
                # Get the information for the document the current invitation is
                # referencing to.
                doc_info = self.manage_DB.get_info('document', rowid=row['docid'])
                # Get the information for the user of the current invitation.
                usr_from = self.manage_DB.get_info('user', rowid=row['userid_from'])

                # Determine the state of the invitation.
                if row['status'] == 1:
                    status = 'Accepted'
                elif row['status'] == 0:
                    status = 'Pending'
                else:
                    status = 'Denied'

                # Create a dictionary with the results and add the dictionary to
                # the list.
                res.append({'id': row['id'], 'docid': doc_info['name'],
                    'userid_from': usr_from['username'],
                    'userid_to': usr_to['username'], 'content': row['content'],
                    'time': datetime.fromtimestamp(int(row['time'])), 'status': status})

            # Return the list of results.
            return res
        # Else the user supplied is a 'Visitor':
        else:
            return []

    def get_invitations_from(self, userid):
        # Get the information for the supplied user.
        usr_from = self.manage_DB.get_info('user', rowid=userid)

        # If the supplied user from is not a 'Visitor':
        if usr_from['usergroup'] != 4:
            # Query for all invitations to the supplied user.
            rows = self.manage_DB.get_info('invitation', where={'userid_from': userid})

            res = []
            for row in rows:
                # Get the information for the document the current invitation is
                # referencing to.
                doc_info = self.manage_DB.ge_info('document', rowid=row['docid'])
                # Get the information for the user of the current invitation.
                usr_to = self.manage_DB.get_info('user', row['userid_from'])

                # Determine the state of the invitation.
                if row['status'] == 1:
                    status = 'Accepted'
                elif row['status'] == 0:
                    status = 'Pending'
                else:
                    status = 'Denied'

                # Create a dictionary with the results and add the dictionary to
                # the list.
                res.append({'id': row['id'], 'docid': doc_info['name'],
                    'userid_from': usr_from['username'],
                    'userid_to': usr_to['username'], 'content': row['content'],
                    'time': datetime.fromtimestamp(int(row['time'])), 'status': status})

            # Return the list of results.
            return res
        # Else the user supplied is a 'Visitor':
        else:
            return []


class DocumentManager:
    BASE_DIR = "dbs"

    def __init__(self, dbm):
        # Save an instance of the database manager.
        self.manage_DB = dbm
        return

    def create_document(self, docid, parent_dir):
        # Get the local file system path for the supplied parent_dir.
        path_logical, path_physical = self.get_document_path(docid)

        # The supplied filename does not exist at the supplied directory.
        if not os.path.exists('%s%s' % (path_physical, docid)):
            # Create the file with the supplied filename.
            fhandle = open('%s%s' % (path_physical, docid), 'w')
            fhandle.close()
            return True
        # The supplied filename does exist at the supplied directory.
        else:
            return False

    def get_document_path(self, docid):
        # Get the information for the supplied document.
        document = self.manage_DB.get_info('document', rowid=docid)

        # The supplied document exist.
        if document:
            # Get the information for the parent directory of the supplied
            # document.
            res = self.manage_DB.get_info('directory',
                rowid=document['parent_dir'])

            path_logical = ''
            path_physical = ''
            # While the parent_dir exist. The parent of the root directory
            # does not exist.
            while res:
                # Add the name/id of the parent directory to the path.
                path_logical = '%s/%s' % (res['name'], path_logical)
                path_physical = 'D%s/%s' % (res['id'], path_physical)
                # Get the information for the parent directory.
                res = self.manage_DB.get_info('directory',
                    rowid=res['parent_dir'])

            return path_logical, path_physical
        # The supplied document does not exist.
        else:
            return '', ''

    def get_directory_documents(self, parent_dir):
        # Query for all the documents in the supplied directory.
        rows = self.manage_DB.get_info('document', where={
            'parent_dir': parent_dir})

        # Get the information for the supplied parent directory.
        dir_info = self.manage_DB.get_info('directory', rowid=parent_dir)

        # Return comments as a list.
        res = []
        for row in rows:
            # If the current document has been suspended:
            if row['infraction'] > 3:
                # Move on to the next document.
                continue

            # Get the information for the owner of the document.
            usr_info = self.manage_DB.get_info('user', rowid=row['owner'])

            # If there was not last modification user:
            if row['last_mod_user'] == 0:
                mod_info = {'username': ''}
            # Else there was a last modification user:
            else:
                # get the information of the last mod user.
                mod_info = self.manage_DB.get_info('user',
                    rowid=row['last_mod_user'])

            # Create a dictionary with the results and add the dictionary to
            # the list.
            res.append({'id': row['id'], 'name': row['name'],
                'parent_dir': dir_info['name'], 'owner': usr_info['username'],
                'infraction': row['infraction'],
                'mod_user': mod_info['username'],
                'mod_time': datetime.fromtimestamp(int(row['last_mod_time'])),
                'size': row['size']})

        # Return the list of results.
        return res


class DirectoryManager:
    BASE_DIR = "dbs"

    def __init__(self):
        self.manage_DB = DBManager()
        return

    def get_directory_path(self, directoryid):
        # Get the information for the supplied directory.
        res = self.manage_DB.get_info('directory', rowid=directoryid)

        path_logical = ''
        path_physical = ''
        # While the parent_dir exist. The parent of the root directory
        # does not exist.
        while res:
            # Add the name/id of the parent directory to the path.
            path_logical = '%s/%s' % (res['name'], path_logical)
            path_physical = 'D%s/%s' % (res['id'], path_physical)
            # Get the information for the parent directory.
            res = self.manage_DB.get_info('directory', rowid=res['parent_dir'])

        return path_logical, path_physical

    def create_directory(self, directoryid):
        # Get the local file system path for the supplied directory.
        path_logical, path_physical = self.get_directory_path(directoryid)

        # The supplied folder name does not exist at the supplied directory.
        if not os.path.isdir('%s' % path_physical):
            # Create the folder with the supplied folder name.
            os.mkdir('%s' % path_physical)
            return True
        # The supplied folder name does exist at the supplied directory.
        else:
            return False

    def get_directory_directories(self, directoryid):
        # Query for all the directories in the supplied directory.
        res = self.manage_DB.get_info('directory', where={
            'parent_dir': directoryid})

        for row in res:
            # Create a dictionary with the results and add the dictionary to
            # the list.
            row['parent'] = self.manage_DB.get_info(
                'directory', rowid=row['parent_dir'])['name']

        # Return the list of results.
        return res


class IndexManager:
    BASE_DIR = "dbs"

    def __init__(self, dbm):
        self.manage_DB = dbm
        return

    def add_index_word(self, root, docid, line, column, branch_word,
        verbose=False):
        # Insert the root word into the index_word table, if the word already
        # exist within the table, the insertion operation will return False,
        # but if it does not exist, the word will be inserted.
        self.manage_DB.insert_info('index_word', insert={'word': root})

        # Search for the root word in the index word table. At this point the
        # word must be in the table, it might have been in the table for a
        # long time or we just inserted it.
        res = self.manage_DB.get_info('index_word', where={'word': root})

        # Get the id of the root word.
        wordid = res[0]['id']

        # Insert a reference with the supplied information and return the
        # the result of the insertion.
        return self.manage_DB.insert_info('index_ref', insert={
            'wordid': wordid, 'docid': docid, 'line': line,
            'column': column, 'branch_word': branch_word}, verbose=verbose)

    def search(self, word):
        # Create an instance of the Porter Stemmer.
        PS = PorterStemmer()

        # Get the information for the supplied word.
        res = self.manage_DB.get_info('index_word', where={
            'word': PS.stem(word, 0, len(word) - 1)})

        # The supplied word exist in the index_word table.
        if res:
            # Extract the id for the supplied word.
            wordid = res[0]['id']

            # Get all the entries in the index reference database that refer to
            # the supplied wordid.
            res = self.manage_DB.get_info('index_ref', where={
                'wordid': wordid})

            # For ever entry in the list.
            for row in res:
                # Modify the current row to contain the stem word.
                row['word'] =  self.manage_DB.get_info(
                    'index_word', rowid=row['wordid'])['word']
                # Modify the current row to contain the document name.
                row['doc'] = self.manage_DB.get_info(
                    'document', rowid=row['docid'])['name']

            # Return the list of all the results.
            return res
        # The supplied word does not exist in the index_word table, so return
        # and empty list.
        else:
            return []

    def index_document(self, docid, path_physical):
        self.manage_DB.delete_references(docid)

        # Get the information for the supplied document.
        document = self.manage_DB.get_info('document', rowid=docid)

        # Open the document for reading.
        fhandle = open('%s%s' % (path_physical, docid), 'r')
        # Create an instance of the Porter Stemmer.
        PS = PorterStemmer()

        # Get the 1st line of the supplied document and force the contents to
        # lowercase.
        content = fhandle.readline().lower()

        # The text widget starts indexing its lines at 1, but columns start
        # indexing at 0.
        line_count = 1

        # While the supplied document has content to be read.
        while content != '':
            # Find all words from the current line of the supplied document
            # and put them in a list.
            words = re.findall('\w+', content)

            # For each word in the list of words from the current line.
            for word in words:
                # Only words whose length is greater than 3 will be indexed.
                if len(word) > 3:
                    # Check for the word in the list of stop words.
                    res = self.manage_DB.get_info('stop_words', where={
                        'word': word})

                    # If the word does not exist in the list of stop words:
                    if not res:
                        # The column of the current word is its index in the
                        # current line.
                        col_count = content.find(word) + 1
                        # Using the PorterStemmer, find the root of the current
                        # word. Add the root word, with the current line and
                        # column number to the index.
                        self.add_index_word(
                            PS.stem(word, 0, len(word) - 1),
                            docid,
                            line_count,
                            col_count,
                            word)
            # Get the next line of the supplied document and force the
            # contents to lowercase.
            content = fhandle.readline().lower()
            # Increment the line count.
            line_count += 1

        # Close the supplied document file.
        fhandle.close()
        return


class AdminManager:

    def __init__(self, dbm):
        # Create an instance of the database manager.
        self.manage_DB = dbm
        return

    def get_pending_applications(self, verbose=False):
        # Get all the applications that has a pending status.
        res = self.manage_DB.get_info('application', where={'status': 0},
            verbose=verbose)

        # If there are any pending applications:
        if res:
            # For each pending application:
            for row in res:
                # Delete the password from the output.
                del(row['password'])
                # Format the time in human readable format.
                row['time'] = datetime.fromtimestamp(int(row['time']))
            # Return the list of pending applications.
            return res
        # Return a empty list.
        return []

    def get_denied_applications(self, verbose=False):
        # Get all the applications that has a denied status.
        res = self.manage_DB.get_info('application', where={'status': -1},
            verbose=verbose)

        # If there are any pending applications:
        if res:
            # For each pending application:
            for row in res:
                # Delete the password from the output.
                del(row['password'])
                # Format the time in human readable format.
                row['time'] = datetime.fromtimestamp(int(row['time']))
            # Return the list of pending applications.
            return res
        # Return a empty list.
        return []

    def get_accepted_applications(self, verbose=False):
        # Get all the applications that has a accepted status.
        res = self.manage_DB.get_info('application', where={'status': 1},
            verbose=verbose)

        # If there are any pending applications:
        if res:
            # For each pending application:
            for row in res:
                # Delete the password from the output.
                del(row['password'])
                # Format the time in human readable format.
                row['time'] = datetime.fromtimestamp(int(row['time']))
            # Return the list of pending applications.
            return res
        # Return a empty list.
        return []

if __name__ == "__main__":
    m = Manager()
    print m.manage_DB.check_rights('directory', 'INSERT')
