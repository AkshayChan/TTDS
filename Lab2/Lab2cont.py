from nltk.corpus import stopwords
from stemming.porter2 import stem
import nltk
import re
idlist = []

with open("CW1collection/trec.5000.txt") as fp, open("preprocess.txt", "w") as fr:
    #Get all the lines in the document
    lis = {}

    #If we come to the ID line, store
    for line in fp:
        if line [0] == "I":
            headtext = ""
            for i in range(2):
                headtext = headtext + fp.next() + " "
            lis.update({line[4:].rstrip() : headtext})
            idlist.append(line[4:])
    """The dictionary here has the word as keys, and another dictionary as the values
    Which have the document IDs as keys and a list of occurences for that word in
    the document as value"""
    dict = {}
    #For each of the text lines (documents)
    for ele in lis:
        #Break out the words in the line, convert to lowercase and preprocess
        linewo = nltk.word_tokenize(lis[ele])
        linewo = [wo for wo in linewo if wo!="TEXT" and wo != "HEADLINE"]
        linewo = [wo.lower() for wo in linewo if wo.isalpha() or wo.isdigit()]
        #and token not in stopwords.words('english')
        linewo = [stem(wo) for wo in linewo]

        #Here we get the respective document index
        doc_index = ele
        #print (doc_index)

        #If a word is in a document, add all of its positions to the dictionary
        for wo in linewo:
            if wo not in dict:
                dict[wo] = {doc_index: [i + 1 for i, x in enumerate(linewo) if x == wo]}
            else:
                dict[wo].update({doc_index: [i + 1 for i, x in enumerate(linewo) if x == wo]})

        #Calculating the total occurences in all documents"""
        #print (dict)

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


with open("preprocess.txt") as fr,  open("CW1collection/queries.boolean.txt") as fq:

    qlis = []

    for line in fq:
        queries = line.split(" ", 1)
        lis.append(queries[1].rstrip())
    #print (qlis)

    for query in qlis:
        retrievedocs = [[]]
        retrivindex = 0
        if "AND" in query or "OR" in query or "NOT" in query:
            words = re.split(" +(AND|OR) +", query)
            i = 0
            andor = 0
            while (i < len(words)):

                #Here we cover the NOT word condition, and iterate the counter by 2 then continue
                #We take out the documents containing this word
                #By subtracting the list of documents containing this word from the list of all document IDs

                if (words[i] == "NOT"):
                    nextwor = words[i+1]
                    nextwor = nextwor.lower()
                    nextwor = stem(nextwor)
                    for x in dict:
                        if x == nextwor:
                            docslist = list(set(idlist) - set(dict[x].keys()))
                            retrievedocs[retrivindex] = docslist
                    retrivindex = retrivindex + 1
                    i = i + 2
                    continue

                #Here we cover the phrase condition
                elif (words[i][0] == "\""):
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
                                    #For all the document IDs in the first  phrase word
                                    #If it is in the list of document IDs for the second phrase word
                                    for srdoc in dict[x]:
                                        if srdoc in dict[y].keys():
                                            #Use that document ID to check the list of occurences
                                            #x + 1 because the first word in the phrase will be
                                            #before the second word in the document
                                            indexlis = [x+1 for x in dict[x][srdoc]]
                                            findlis = [x for x in dict[y][srdoc]]
                                            #If both the lists contain the same element, we have a phrase match
                                            if len([x for x in indexlis if x in findlis]) != 0:
                                                retrievedocs[retrivindex].extend(srdoc)
                    retrivindex = retrivindex + 1
                    i = i + 1
                    continue

                elif(words[i] == "AND"):
                    andor = 0
                    i = i + 1
                    continue

                elif(words[i] == "OR"):
                    andor = 1
                    i = i + 1
                    continue

                #If we come accross just a simple string
                #Find all the documents that have it
                else:
                    wor = words[i]
                    wor = nextwor.lower()
                    wor = stem(nextwor)
                    for x in dict:
                        if x == nextwor:
                            retrievedocs[retrivindex] = dict[x].keys()
                    i = i + 1
                    continue

            #End while loop
            if (andor == 0):
                print (list(set(retrievedocs[0]) & set(retrievedocs[1])))
            elif (andor == 1):
                print (list(set().union(retrievedocs[0], retrievedocs[1])))
        elif (query[0] == "#"):
