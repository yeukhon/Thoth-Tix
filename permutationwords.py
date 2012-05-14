def permwords(word, verbose=False):
    Listofwords = []
    delwords = []# list of words with one char deleted
    flipwords = [] #flip one char for all possible combos (transposition)
    alterwords = []#change 1 char for all possible combos
    a=('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z')

    if len(word) == 1:# There is only one possible permutation
        Listofwords.append(word)
    else:
        #for i in a:
        for pos in range(len(word)): #print pos #this prints 0,1,2,3,4 for now
            delwords.append(word[0:pos]+word[pos+1:len(word)]) #list of words where each char has been deleted one at a time; if word is 'spell' it generates: pell, sell, spll, spel, spel
            if verbose: print 'Delwords', delwords

            flipwords.append(word[0:pos]+word[pos+1:pos+2]+word[pos:pos+1] +word[pos+2:len(word)]) #this prints psell, sepll, splel, spell, spell
            #print flipwords

            flipwords.append(word[0:pos]+word[pos+2:pos+3]+word[pos+1:pos+2]+word[pos:pos+1]+word[pos+3:len(word)]) #this prints epsll, slepl, splle,spell, spell
            #print flipwords

            flipwords.append(word[0:pos]+word[pos+3:pos+4]+word[pos+1:pos+3]+word[pos:pos+1] +word[pos+4:len(word)]) #this prints lpesl, slelp, splle, spell, spell
            #print flipwords

            flipwords.append(word[0:pos]+word[pos+4:pos+5]+word[pos+1:pos+4]+word[pos:pos+1] +word[pos+5:len(word)]) #this prints lpels, sellp, splle, spell, spell
            #print flipwords

        for i in a:
            for pos in range(len(word)):
                alterwords.append((word[:pos]+i+word[pos+1:len(word)]))
        if verbose: print 'Alterwords:', alterwords

		Listofwords.extend(delwords)
		Listofwords.extend(flipwords)
		Listofwords.extend(alterwords)
		Listofwords = list(set(Listofwords))

	if verbose:
		print 'Giant List %i: %s' % (len(Listofwords), Listofwords)


if __name__ == "__main__":
	permwords('spell', verbose=True)
