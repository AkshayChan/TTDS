from nltk.corpus import stopwords
from stemming.porter2 import stem
import nltk
file_content = open("collections/sample.txt").read()
tokens = nltk.word_tokenize(file_content)
tokens = [token.lower() for token in tokens if token.isalpha() and token not in stopwords.words('english')]
#tokens = [stem(token) for token in tokens]
tokens = [token for token in tokens if token != "id" and token != "text"]
output = set(tokens)
tokens = list(output)

with open("collections/sample.txt") as fp, open("preprocess.txt", "w") as fr:
    #Get all the lines in the document
    lis = []
    '''for line in fp:
        if line[0] != "I" and line[0] != "T":
            lis.append(line + " " + fp.next())'''
    for line in fp:
        if line[0] != "I":
            lis.append(line)

    """The dictionary here has the word as keys, and another dictionary as the values
    Which have the document IDs as keys and a list of occurences for that word in
    the document as value"""
    dict = {}
    #For each of the text lines (documents)
    for ele in lis:
        #Break out the words in the line, convert to lowercase and preprocess

        linewo = nltk.word_tokenize(ele)
        linewo = [wo for wo in linewo if wo!="TEXT" and wo != "HEADLINE"]
        linewo = [wo.lower() for wo in linewo if wo.isalpha()]
        #Here we get the respective document index
        doc_index = (lis.index(ele) + 1)
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

f = open("output.txt", "a")
f.write(", ".join(tokens))
f.close()
