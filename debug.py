from user import User, Guest, RegularUser, SuperUser
from document import Document
from md5 import new
from time import time

def run():
    # Debugging:
    verbose = False
    guest = Guest()
    admin = SuperUser(2)

    ###########################################################################
    # TD1 = Register as Guest
    ###########################################################################
    res = guest.register('Ash', 'pika',  'AKetchum@pokemon.com',
        'Ash Ketchum Reporting In!', verbose=verbose)
    print 'Registering as Guest:', res

    ###########################################################################
    # TD2 = Accept Application as SuperUser
    ###########################################################################
    # Get the id for the inserted application.
    appid = admin.manage.manage_DB.get_info('application', where={
        'username': 'Ash', 'email': 'AKetchum@pokemon.com'},
        verbose=verbose)[0]['id']
    # Accept the application.
    res = admin.accept_application(appid, verbose=verbose)
    print 'Accept Application as SuperUser:', res

    ###########################################################################
    # TD3 = Create an instance of Ash
    ###########################################################################
    # Create an instance of the User class for the newly created user, when the
    # admin accepts an application, the user is automatically created.
    ash = RegularUser(username='Ash')

    ###########################################################################
    # TD4 = Create an directory as Ash
    ###########################################################################
    # Add a directory at the root directory.
    root = 1
    res = ash.create_new_directory('Team', root, verbose=verbose)
    print 'Create Directory as Ash:', res

    ###########################################################################
    # TD5 = Create a document as Ash
    ###########################################################################
    # Get the dirid for the created directory.
    teamid = ash.manage.manage_DB.get_info('directory', where={
        'name': 'Team', 'parent_dir': root}, verbose=verbose)[0]['id']
    # Create a document at the directory 'Team'.
    res = ash.create_new_document('Pikachu.txt', teamid, verbose=verbose)
    print 'Create Document as Ash:', res

    ###########################################################################
    # TD6 =  Comment as Guest
    ###########################################################################
    # Get the 'id' of the newly created document.
    pikaid = ash.manage.manage_DB.get_info('document', where={
        'name': 'Pikachu.txt', 'parent_dir': teamid}, verbose=verbose)[0]['id']
    res = guest.comment(pikaid, "Pikachu use Thunderbolt!",verbose=verbose)
    print 'Comment as Guest:', res

    ###########################################################################
    # TD7 =  Comment as Ash
    ###########################################################################
    res = ash.comment(pikaid, "Pikachu use Thunder!",verbose=verbose)
    print 'Comment as Ash:', res

    ###########################################################################
    # TD8 =  Complain as Guest
    ###########################################################################
    res = guest.complain(pikaid, "Pikachu is not obeying me!",verbose=verbose)
    print 'Complain as Guest:', res

    ###########################################################################
    # TD9 =  Complain as Ash
    ###########################################################################
    res = ash.complain(pikaid, "Pikachu, you so crazy!",verbose=verbose)
    print 'Complain as Ash:', res

    ###########################################################################
    # TD10 =  Send an Invitation from Ash to admin
    ###########################################################################
    res = ash.send_invitation_to(pikaid, admin.info['id'], 'Train my Pikachu.',
        verbose=verbose)
    print 'Invitation from Ash to admin:', res

    ###########################################################################
    # TD11 = Create an instance of Pikachu
    ###########################################################################
    # Create an instance of the User class for the newly created document.
    pikachu = Document(pikaid)

    ###########################################################################
    # TD12 = Add sample content to Pikachu
    ###########################################################################
    # Create a handle to Pikachu.
    fhandle = open('%s%s' % (pikachu.info['ppath'], pikaid), 'w')
    # Write sample content to the file.
    fhandle.write("""An orange is a type of citrus fruit which people often eat. Oranges are a very good source of vitamins, especially vitamin C. Orange juice is an important part of many people's breakfast. The "sweet orange", which is the kind that are most often eaten today, grew first in Asia but now grows in many parts of the world.""")
#~
#~ Oranges are round orange-coloured fruit that grow on a tree which can reach 10 metres high. Orange trees have dark green shiny leaves and small white flowers with five petals. The flowers smell very sweet which attracts many bees.
#~
#~ An orange has a tough shiny orange skin. Inside, the fruit is divided into "segments", which have thin tough skins that hold together many little sections with juice inside. There are usually ten segments in an orange, but sometimes there are more. Inside each segment of most types of orange there are seeds called "pips". Orange trees can be grown from pips, but some types of orange trees can only be grown from "cuttings" (a piece cut off a tree and made to grow roots). The segments and the skin are separated by white stringy fibrous material called "pith". In most types of oranges, the skin can be peeled off the pith, and the segments can be pulled apart with the fingers to be eaten. In some oranges it is hard to take the skin off. With mandarin oranges, the skin, pith and segments can all be pulled apart very easily. Orange skin is often called "orange peel".
#~
#~ Oranges are an important food source in many parts of the world for several reasons. They are a commonly available source of vitamin C. The juice is a refreshing drink. They last longer than many other fruits when they are stored. They are easy to transport because each orange comes in its own tough skin which acts as a container. They can be piled into heaps or carried in bags, lunchboxes and shipping containers without being easily damaged.""")
    fhandle.close()

    ##########################################################################
    # TD13 =  Index Pikachu
    ###########################################################################
    res = pikachu.create_index()
    print 'Indexing Pikachu:', res

    ###########################################################################
    # TD14 = Search Pikachu
    ###########################################################################
    res = ash.manage.manage_Indx.search('orange')
    for i in res:
        print 'Word: %s\tLine: %s\tCol: %s' % (i['branch_word'], i['line'], i['column'])

    return

if __name__ == "__main__":
    run()
