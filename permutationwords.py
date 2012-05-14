from database import Database #same directory, database is module, Database is class
from operator import itemgetter

def permwords(userid, word):
  Listofwords=[]
  delwords=[]# list of words with one char deleted
  flipwords=[]#flip one char for all possible combos (transposition)
  alterwords=[]#change 1 char for all possible combos
  a=[] #list of a-z, used for alterwords
  a=('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z')
  if len(word) == 1:# There is only one possible permutation
    Listofwords.append(word)
  else:
    # #for i in a:
    for pos in range(len(word)): #print pos #this prints 0,1,2,3,4 for now
        delwords.append((word[0:pos]+word[pos+1:len(word)])) #list of words where each char has been deleted one at a time; if word is 'spell' it generates: pell, sell, spll, spel, spel
         #print delwords

        flipwords.append((word[0:pos]+word[pos+1:pos+2]+word[pos:pos+1] +word[pos+2:len(word)])) #this prints psell, sepll, splel, spell, spell
        # #print flipwords

        flipwords.append((word[0:pos]+word[pos+2:pos+3]+word[pos+1:pos+2]+word[pos:pos+1]+word[pos+3:len(word)])) #this prints epsll, slepl, splle,spell, spell
        # #print flipwords

        flipwords.append((word[0:pos]+word[pos+3:pos+4]+word[pos+1:pos+3]+word[pos:pos+1] +word[pos+4:len(word)])) #this prints lpesl, slelp, splle, spell, spell
        # #print flipwords

        flipwords.append((word[0:pos]+word[pos+4:pos+5]+word[pos+1:pos+4]+word[pos:pos+1] +word[pos+5:len(word)])) #this prints lpels, sellp, splle, spell, spell
        # #print flipwords


    for i in a:
        for pos in range(len(word)):
            alterwords.append((word[:pos]+i+word[pos+1:len(word)]))
         # #print alterwords

    for d in delwords:
        if d not in Listofwords: #only adds those words that aren't already in Listofwords, this eliminates repetition of words
             Listofwords.append(d)
    #print Listofwords

    for f in flipwords:
        if f not in Listofwords:
            Listofwords.append(f)
    #print Listofwords

    for al in alterwords:
        if al not in Listofwords:
            Listofwords.append(al)
    #print Listofwords

    topfive=[] # this is the list of only the top 5 permutated words with the highest frequency that match the dictionary
    sortedlist=[]	#this is the sorted list of all the permutated words that match the dictionary
    resultdict=[] # this is the list of all the permutated words that match the dictionary
    db = Database()
    #res = db._get_info('frequency', where={'word': value})
    for i in Listofwords:
        res = db._get_info('frequency', where={'word': i})
        if res: #if result is not blank
            resultdict.append(res[0])#resultdict=res[0]

    for i in Listofwords:
        res = db._get_info('X%s' % userid, where={'word': i})
        if res: #if result is not blank
            res[0]['frequency'] = 1
            resultdict.append(res[0])#resultdict=res[0]

    #print resultdict #['frequency'] >regular one item dictionary
    sortedlist = sorted(resultdict,key=itemgetter('frequency'), reverse=True)
    #print sortedlist[:4]
    topfive=sortedlist[:4]
    for i in topfive:
        print i['word']

    return topfive


#~ permwords(2, 'theae')
