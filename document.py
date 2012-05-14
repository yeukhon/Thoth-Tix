from manage import Manager
from sqlite3 import connect
from datetime import datetime
import time
import os
import re
import json


class Document:

    def __init__(self, ID):
        # Create an instance of the Manager class.
        self.manage = Manager()
        self.manage.manage_DB.update_user_info(self.manage.manage_DB.get_info(
            'user', where={'id': 2})[0])

        # Get the current information for the supplied document ID.
        self.info = self.manage.manage_DB.get_info('document', rowid=ID)

        # Get the local and physical file system path for the document.
        path_logical, path_physical = self.manage.manage_Docs.get_document_path(
            self.info['id'])
        self.info['lpath'] = path_logical
        self.info['ppath'] = path_physical
        return

    def init_autocompleteDB(self):
        # Reset the autocomplete table.
        self.manage.manage_DB.init_table_autocomplete()

        # Open the document for reading.
        fhandle = open('%s%s' % (self.info['ppath'], self.info['id']), 'r')

        # Get the contents of the supplied document and force the contents to
        # lowercase.
        content = fhandle.read().lower()

        # Find all the words in the supplied content.
        words = re.findall('\w+', content)

        for word in words:
            # Only words with a length greater than 3 character will be used
            # as suggestions.
            if len(word) > 3:
                # Insert the word into the autocomplete table.
                self.manage.manage_DB.insert_info('autocomplete', insert={
                    'word': word})
        return

    def suggest_word(self, fragment):
        # Return the suggested word from the database.
        return self.manage.manage_DB.suggest_word_autocompleteDB(fragment)

    def insert_word_autocompleteDB(self, word):
        # Insert the supplied word.
        res = self.manage.manage_DB.insert_info('autocomplete', insert={
            'word': word})

        # If the insertion was successful:
        if res:
            # Return True to denote success.
            return True
        # Else the insertion was unsuccessful:
        else:
            # Return False to denote failure.
            return False

    def create_index(self):
        # Index the current document.
        res = self.manage.manage_Indx.index_document(self.info['id'],
            self.info['ppath'])

        # If the insertion was successful:
        if res:
            # Return True to denote success.
            return True
        # Else the insertion was unsuccessful:
        else:
            # Return False to denote failure.
            return False

    def get_document_comments(self, docid):
        # Query for all comments for the supplied document.
        rows = self.manage.manage_DB.get_info('comment', where={'docid': docid})

        # Get the information for the supplied document.
        doc_info = self.manage.manage_DB.get_info('document', rowid=docid)

        # Return comments as a list.
        res = []
        for row in rows:
            # Get the information for the user that wrote the comment.
            usr_info = self.manage.manage_DB.get_info('user', rowid=row['userid'])

            # Create a dictionary with the results and add the dictionary to
            # the list.
            res.append({'id': row['id'], 'doc': doc_info['name'],
                'user': usr_info['username'], 'content': row['content'],
                'time': datetime.fromtimestamp(int(row['time']))})

        # Return the list of results.
        return res

    def get_document_complaints(self):
        docid = self.info['id']
        # Query for all complaints for the supplied document.
        rows = self.manage.manage_DB.get_info('complaint', where={
            'docid': docid})

        # Get the information for the supplied document.
        doc_info = self.manage.manage_DB.get_info('document', rowid=docid)

        # Return comments as a list.
        res = []
        for row in rows:
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
    def is_owner(self, userid):
        docid = self.info['id']
        res = self.manage.manage_DB.get_info('document', rowid=docid)
        print 'is_owner', res, 'userid', userid
        if res['owner'] == userid:
            return True
        else:
            return False

    def is_member(self, userid):
        docid = self.info['id']
        # The supplied user is the owner of the supplied document.
        res = self.manage.manage_DB.get_info('document', rowid=docid)
        if res['owner'] == userid:
            return True

        # Search for a member entry with the supplied user for the supplied
        # document.
        res = self.manage.manage_DB.get_info('member', where={
            'userid': userid, 'docid': docid})

        # There exist a member entry for the supplied user.
        if res:
            return True
        # There does not exist a member entry for the supplied user.
        else:
            return False

    def save(self, content, userid, verbose=False):
        import difflib
        # Create a handler to the file to read.
        fhandle = open('%s%s' % (self.info['ppath'], self.info['id']), 'r')

        # Get the contents of the file and close the handler.
        old = fhandle.read().splitlines()
        fhandle.close()

        # Create a handler to the file to write. Write the new contents to the
        # file and close the handler.
        fhandle = open('%s%s' % (self.info['ppath'], self.info['id']), 'w')
        fhandle.write(content)
        fhandle.close()

        # Calculate the difference between the file and new content.
        content = content.splitlines()
        diffs = difflib.Differ().compare(old, content)

        output = []
        count = 0
        # For each line of the file:
        for line in diffs:
            # If the line has been removed:
            if line[0:2] == '- ':
                # Find the line count.
                count = old.index(line[2:]) + 1
                # Add the diff and line number to the output list.
                output.append('- %i %s' % (count, line[2:].replace('\n', '')))
            # Else if the line has been added:
            elif line[0:2] == '+ ':
                # Increment the line count.
                count += content[count:].index(line[2:]) + 1
                # Add the diff and line number to the output list.
                output.append('+ %i %s' % (count, line[2:].replace('\n', '')))
        print '\n'.join(output)

        # If the supplied filename does not exist at the supplied directory:
        if not os.path.exists('%sM%s' % (self.info['ppath'], self.info['id'])):
            mhandle = open('%sM%s' % (self.info['ppath'], self.info['id']), 'w')
            mod = [{'userid': userid, 'time': time.time(), 'content': output}]
            # Write the output to the mod file.
            mhandle.write(json.dumps(mod))
            mhandle.close()
        # Else the mod file for the supplied document already exist:
        else:
            # Create a handler for the mod file.
            mhandle = open('%sM%s' % (self.info['ppath'], self.info['id']), 'r')

            # Get the contents of the mod file as a json object.
            mod = json.loads(mhandle.read())
            mhandle.close()

            # Append the current modification to the end of the json object.
            mod.append({
                'userid': userid, 'time': time.time(), 'content': output})
            # If there are more than 3 modifcations in the file:
            if len(mod) > 3:
                # Remove the modification from the beginning of the json object.
                mod.pop(0)

            # Create a handler for the mod file, write the output to the file, and
            # close the handler.
            mhandle = open('%sM%s' % (self.info['ppath'], self.info['id']), 'w')
            mhandle.write(json.dumps(mod))
            mhandle.close()

        # Update the document information with the last mod user and time.
        self.manage.manage_DB.update_info('document', update={
            'last_mod_user': userid,
            'last_mod_time': time.time(),
            'size': os.path.getsize('%s%s' % (self.info['ppath'], self.info['id']))},
            where={'id': self.info['id']}, verbose=verbose)

        # Index the document.
        self.create_index()
        return True

if __name__ == '__main__':
    from user import RegularUser
    ru = RegularUser(3)
    verbose = False

    ###########################################################################
    # TD1 = Create a Document
    ###########################################################################
    # Create a document at the root directory.
    res = ru.create_new_document('TDoc1.txt', 1, verbose=verbose)
    print 'Create Document:', res

    # Get the 'id' of the newly created document.
    docid = ru.manage.manage_DB.get_info('document', where={
        'name': 'TDoc1.txt', 'parent_dir': 1}, verbose=verbose)[0]['id']
    # Create an instance of the Document class for the newly created document.
    doc = Document(docid)
    print 'Document info:', doc.info

    # Create a handle to the document.
    fhandle = open('%s%s' % (doc.info['ppath'], docid), 'w')
    # Write sample content to the file.
    content = ''#'An orange is a type of citrus fruit.'
    fhandle.write(content)
    fhandle.close()

    # Content has been added to the file.
    res = doc.save("Good Morning!\nGood Morning to you!\nHow do you do?\nFine thank you, yourself?\nI am well.\nGoodbye.\nGoodbye.", 3)#content+'\nHello world!', 3)
    print 'Saving Document:', res
    # Content has been removed to the file.
    res = doc.save("Good Morning!\nHow do you do?\nI am well.\nGoodbye.", 3)#content+'\nHello world!', 3)
    print 'Saving Document:', res

    doc.manage.manage_DB.print_DB('document')
