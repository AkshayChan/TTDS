from nltk.corpus import stopwords
from stemming.porter2 import stem
import nltk

with open("collections/trec.sample.txt") as fp, open("preprocess.txt", "w") as fr:
    #Get all the lines in the document
    lis = {}

    #If we come to the ID line, store
    for line in fp:
        if line [0] == "I":
            headtext = ""
            for i in range(2):
                headtext = headtext + fp.next() + " "
            lis.update({line[4:] : headtext})
    """The dictionary here has the word as keys, and another dictionary as the values
    Which have the document IDs as keys and a list of occurences for that word in
    the document as value"""
    dict = {}
    #For each of the text lines (documents)
    for ele in lis:
        #Break out the words in the line, convert to lowercase and preprocess
        linewo = nltk.word_tokenize(lis[ele])
        linewo = [wo for wo in linewo if wo!="TEXT" and wo != "HEADLINE"]
        linewo = [wo.lower() for wo in linewo if wo.isalnum()]
        #and token not in stopwords.words('english')
        #tokens = [stem(token) for token in tokens]

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
