from stemming.porter2 import stem
import nltk
import re
import math
import operator

#idlist has the list of all the document ids
idlist = []

#The dictionary here has the word as keys, and another dictionary as the values
#Which have the document IDs as keys and a list of occurences for that word in
#the document as value
dict = {}

stopwordsli = []

'''Module 1 - creating the indexes for the words in the document'''

with open("CW1collection/trec.5000.txt") as fp, open("preprocess.txt", "w") as fr, open ("CW1collection/stopwords.txt") as fil:

    #Get all the lines in the document in a dictionary with ID as key and HEADLINE/TEXT as value
    lis = {}

    #If we come to the ID line, store the next two lines in the dictionary
    #Store the document ID as the key and the HEADLINE and TEXT lines as value
    #Also create a list of all documents
    for line in fp:
        if line [0] == "I":
            headtext = ""
            for i in range(2):
                headtext = headtext + fp.next() + " "
            lis.update({line[4:].rstrip() : headtext})
            idlist.append(line[4:].rstrip())

    for lines in fil:
        stopwordsli.append(lines.rstrip())

    print(stopwordsli)

    #For each of the text lines (documents) (headline plus text)
    for ele in lis:

        #Break out the words in the line, convert to lowercase and preprocess (alphanumeric, lowercase, stopwrods, stemming)
        linewo = nltk.word_tokenize(lis[ele])
        linewo = [wo for wo in linewo if wo!="TEXT" and wo != "HEADLINE"]
        linewo = [wo.lower() for wo in linewo if wo.isalpha() or wo.isdigit()]
        linewo = [stem(wo) for wo in linewo if wo not in stopwordsli]

        #Here we get the respective document index
        doc_index = ele
        #print (doc_index)

        #If a word is in a document, add all of its positions in that document to the dictionary
        #If word already in the dictionary, update the positions
        for wo in linewo:
            if wo not in dict:
                dict[wo] = {doc_index: [i + 1 for i, x in enumerate(linewo) if x == wo]}
            else:
                dict[wo].update({doc_index: [i + 1 for i, x in enumerate(linewo) if x == wo]})

    #Write the first file

    for x in dict:
            #Writing the word
            fr.write (str(x) + ":")
            fr.write ("\n")
            #Now we write it's document IDs and it's occurences in them
            for y in dict[x]:
                fr.write("\t")
                fr.write(str(y) + ":" + " ")
                fr.write(",".join([str(i) for i in dict[x][y]]))
                fr.write("\n")
            fr.write("\n")

fp.close()
fr.close()

'''Module 2 - reloading the index into memory and running boolean, phrase and prximity search'''

with open("preprocess.txt") as fr,  open("CW1collection/queries.boolean.txt") as fq, open("results.boolean.txt", "w") as fil:

    qlis = []
    j = 1

    #First we extract the queries and remove the newline in the beginning
    for line in fq:
        queries = line.split(" ", 1)
        qlis.append(queries[1].rstrip())
    #print (qlis)

    for query in qlis:
        retrievedocs = [[]]
        retrivindex = 0
        #print(query[0])

        #If we have a Boolean seach query
        if "AND" in query or "OR" in query or "NOT" in query:
            words = re.split(" +(AND|OR) +", query)
            print (words)
            i = 0
            andor = 0
            while (i < len(words)):

                #Here we cover the NOT word condition, and iterate the counter by 2 then continue
                #We take out the documents containing this word
                #By subtracting the list of documents containing this word from the list of all document IDs
                if (words[i][0:3] == "NOT"):
                    nextwor = words[i].split()[1]
                    nextwor = nextwor.lower()
                    nextwor = stem(nextwor)
                    print ("Got the NOT word")
                    print(nextwor)
                    #Retrivindex can be updated inside the loop since we will only find the word once.
                    #Subtract the list of documents containing the word from list of all documents
                    for x in dict:
                        if x == nextwor:
                            docslist = list(set(idlist) - set(dict[x].keys()))
                            retrievedocs.insert(retrivindex, docslist)
                    retrivindex = retrivindex + 1
                    i = i + 1
                    continue

                #Here we cover the phrase condition
                elif (words[i][0] == "\""):
                    #Remove the quotes in the string and preprocess
                    phrasewords = words[i].replace('"', '')
                    phraselist = phrasewords.split()
                    phraselist = [prh.lower() for prh in phraselist]
                    phraselist = [stem(prh) for prh in phraselist]
                    for x in dict:
                        #If we have found the first word in the dictionary
                        if x == phraselist[0]:
                            #If we have found the second word in the dictionary
                            for y in dict:
                                if y == phraselist[1]:
                                    print ("Phrase search inside AND OR")
                                    print (phraselist[0])
                                    print (phraselist[1])
                                    #For all the document IDs in the first  phrase word
                                    #If it is in the list of document IDs for the second phrase word
                                    for srdoc in dict[x]:
                                        if srdoc in dict[y].keys():
                                            #Use that document ID to check the list of occurences
                                            #x + 1 because the first word in the phrase will be
                                            #before the second word in the document
                                            #print(x)
                                            #print(srdoc)
                                            indexlis = [a+1 for a in dict[x][srdoc]]
                                            findlis = [b for b in dict[y][srdoc]]
                                            #If both the lists contain the same position, we have a phrase match
                                            if len([c for c in indexlis if c in findlis]) != 0:
                                                #If we have already found one document ID for this phrase
                                                #extend that list with more indexes
                                                if (retrievedocs[retrivindex]):
                                                    retrievedocs[retrivindex].extend([srdoc])
                                                #if we haven't, create a list of indexes
                                                else:
                                                    retrievedocs.insert(retrivindex, [srdoc])
                    retrivindex = retrivindex + 1
                    i = i + 1
                    continue

                elif(words[i] == "AND"):
                    andor = 1
                    i = i + 1
                    continue

                elif(words[i] == "OR"):
                    andor = 2
                    i = i + 1
                    continue

                #If we come accross just a simple string
                #Find all the documents that have it
                else:
                    wor = words[i]
                    wor = wor.lower()
                    wor = stem(wor)
                    #Retrivindex can be updated inside the loop since we will only find the word once.
                    for x in dict:
                        if x == wor:
                            print ("Got the individual words")
                            print (x)
                            retrievedocs.insert(retrivindex, dict[x].keys())
                    retrivindex = retrivindex + 1
                    i = i + 1
                    continue

            #After we have parsed through the entire query
            finalist = []
            #If we have no ANDs/ORs in the list
            if (andor == 0):
                finalist = retrievedocs[0]
            #If AND, take an intersection
            elif (andor == 1):
                finalist = list(set(retrievedocs[0]) & set(retrievedocs[1]))
            #If OR, take an union
            elif (andor == 2):
                finalist = list(set().union(retrievedocs[0], retrievedocs[1]))

            #Write the document IDs to the file
            finalist = sorted(list(set(finalist)))
            for fid in finalist:
                fil.write(str(j) + " " + "0" + " " + str(fid) + " " + "0" + " " + "1" + " " + "0" + "\n")

        #Here we implement proximity search. We first extract the number out from the query
        #Then we get the individual words and search for the common document
        #containg both words, the same way we did phrase search
        elif (query[0] == "#"):

            #Get the number out by splitting on the opening bracket and replacing the hash
            proxindex = query.split('(')[0]
            proxindex = proxindex.replace('#', '')
            print(proxindex)

            #Replace the comma between the words with a space and split on that.
            proxwords = query.replace('#', '').replace('(', '').replace(')', '').replace(',', ' ')
            proxwords = re.sub('\d', '', proxwords)
            proxlist = proxwords.split()

            #Then do the preprocessing on the words
            proxlist = [prh.lower() for prh in proxlist]
            proxlist = [stem(prh) for prh in proxlist]
            print(proxlist)
            for x in dict:
                #If we have found the first word in the dictionary
                if x == proxlist[0]:
                    #If we have found the second word in the dictionary
                    for y in dict:
                        if y == proxlist[1]:
                            #For all the document IDs in the first word
                            #If it is in the list of document IDs for the second word
                            for srdoc in dict[x]:
                                if srdoc in dict[y].keys():
                                    #Use that document ID to check the list of occurences
                                    indexlis = [a for a in dict[x][srdoc]]
                                    findlis = [b for b in dict[y][srdoc]]
                                    #If the difference in position for any two ocurences is less than 15
                                    #We have a proximity match
                                    for a in indexlis:
                                        for b in findlis:
                                            if abs(int(a)-int(b)) <=proxindex:
                                                #If we have already found one document ID for this phrase
                                                #extend that list with more indexes
                                                if (retrievedocs[0]):
                                                    retrievedocs[0].extend([srdoc])
                                                #if we haven't, create a list of indexes
                                                else:
                                                    retrievedocs.insert(0, [srdoc])

            #Write the document IDs to the file
            finalist = sorted(list(set(retrievedocs[0])))
            for fid in finalist:
                fil.write(str(j) + " " + "0" + " " + str(fid) + " " + "0" + " " + "1" + " " + "0" + "\n")

        #The case where we simply find a phrase just like this
        elif (query[0] == "\""):
            #Remove the quotes in the string and preprocess
            phrasewords = query.replace('"', '')
            phraselist = phrasewords.split()
            phraselist = [prh.lower() for prh in phraselist]
            phraselist = [stem(prh) for prh in phraselist]
            for x in dict:
                #If we have found the first word in the dictionary
                if x == phraselist[0]:
                    #If we have found the second word in the dictionary
                    for y in dict:
                        if y == phraselist[1]:
                            print ("Phrase search only - Got the words")
                            print (phraselist[0])
                            print (phraselist[1])
                            #For all the document IDs in the first  phrase word
                            #If it is in the list of document IDs for the second phrase word
                            for srdoc in dict[x]:
                                if srdoc in dict[y].keys():
                                    #Use that document ID to check the list of occurences
                                    #x + 1 because the first word in the phrase will be
                                    #before the second word in the document
                                    #print(x)
                                    #print(srdoc)
                                    indexlis = [a+1 for a in dict[x][srdoc]]
                                    findlis = [b for b in dict[y][srdoc]]
                                    #If both the lists contain the same position, we have a phrase match
                                    if len([c for c in indexlis if c in findlis]) != 0:
                                        #If we have already found one document ID for this phrase
                                        #extend that list with more indexes
                                        if (retrievedocs[0]):
                                            retrievedocs[0].extend([srdoc])
                                        #if we haven't, create a list of indexes
                                        else:
                                            retrievedocs.insert(0, [srdoc])

            #Write the document IDs to the file
            finalist = sorted(list(set(retrievedocs[0])))
            for fid in finalist:
                fil.write(str(j) + " " + "0" + " " + str(fid) + " " + "0" + " " + "1" + " " + "0" + "\n")

        #We have a simple string only to match
        else:
            wor = query
            wor = wor.lower()
            wor = stem(wor)
            #Retrivindex does not need to be updated
            for x in dict:
                if x == wor:
                    retrievedocs[0] = dict[x].keys()

            #Write the document IDs to the file
            finalist = sorted(list(set(retrievedocs[0])))
            for fid in finalist:
                fil.write(str(j) + " " + "0" + " " + str(fid) + " " + "0" + " " + "1" + " " + "0" + "\n")

        j = j + 1

    fr.close()
    fp.close()
    fil.close()
    #End of the module doing phrase, proximity and boolean search

''' Module 3, reloading the index into memory and creating the ranked IR '''

with open("preprocess.txt") as fr,  open("CW1collection/queries.ranked.txt") as fq, open("results.ranked.txt", "w") as fil:

    qlis = []

    #First we extract the queries and remove the newline in the end
    for line in fq:
        queries = line.split(" ", 1)
        qlis.append(queries[1].rstrip())

    i = 1
    #Iterating through the query
    for query in qlis:

        tflist = {}
        #Preprocess the words
        wordsq = query.split()
        wordsq = [wor.lower() for wor in wordsq]
        wordsq = [stem(wor) for wor in wordsq if wor not in stopwordsli]

        #Replace any special characters in the word first
        for wor in wordsq:
            for char in wor:
                if char in "?.!/;:":
                    wor = wor.replace(char,'')

        #iterating through the list of all documents
        for idn in idlist:
            tfsum = 0
            for wor in wordsq:
                for x in dict:
                    if x == wor:
                        #If the document ID is in the IDs for our word
                        if idn in dict[x].keys():
                             #Document frequency is simply the number of documents the term occured in
                             dffreq = len(dict[x].keys())
                             #Term frequency for that document is the total times the term occured in this document
                             tffreq = len(dict[x][idn])
                             #Adding the frequency for this term to the tfidf sum for the document
                             tfsum = tfsum + ((1 + math.log10(tffreq)) * math.log10(len(idlist)/dffreq))
                             tfsum = round(tfsum, 4)
            #Write every single tfidf of every matched document to the file
            if tfsum != 0:
                tflist.update({idn: tfsum})

        #Have a list of tuples to make sure it is sorted
        sorted_dicdata = sorted(tflist.items(), key=operator.itemgetter(1),reverse=True)

        #Write the values to the file
        #Make sure we don't have more than 1000 results per query
        res = 0
        for ite,val in sorted_dicdata:
            if (res < 1000):
                fil.write(str(i) + " " + "0" + " " + str(ite) + " " + "0" + " " + str(val) + " " + "0" + "\n")
            res = res + 1
        i = i + 1

print (len(dict.keys()))
