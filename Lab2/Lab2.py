
#from nltk.tokenize import word_tokenize
#with open ('pg10.txt') as fin, open('output.txt', "a") as fout:
    #tokens = word_tokenize(line)
    #fout.write("\n".join(tokens))

from nltk.corpus import stopwords
from stemming.porter2 import stem
import nltk
file_content = open("collections/trec.sample.txt").read()
tokens = nltk.word_tokenize(file_content)
tokens = [token.lower() for token in tokens if token.isalpha() and token not in stopwords.words('english')]
#tokens = [stem(token) for token in tokens]
tokens = [token for token in tokens if token != "id" and token != "text"]
output = set(tokens)
tokens = list(output)

with open("collections/trec.sample.txt") as fp, open("preprocess.txt", "w") as fr:
    lis = []
    for line in fp:
        if line[0] != "I":
            lis.append(line)
    for word in tokens:
        dict = {}
        #For each of the text lines
        for ele in lis:
            #Break out the words in the line, convert to lowercase and preprocess
            linewo = nltk.word_tokenize(ele)
            linewo = [wo for wo in linewo if wo!="TEXT" and wo != "HEADLINE"]
            linewo = [wo.lower() for wo in linewo if wo.isalpha()]
            #Here we sa
            doc_index = (lis.index(ele) + 1)
            #If the word is in the document, add all of its positions
            if word in linewo:
                dict[doc_index] = [i for i, x in enumerate(linewo) if x == word]
        #print (word)
        #print (dict)
        #Calculating the total occurences in all documents
        sum = 0
        for x in dict:
            sum = sum + len(dict[x])
        #Writing the word and the
        fr.write (str(word) + ":" + " " + "(" + str(sum) + ")")
        fr.write ("\n")
        for x in dict:
            fr.write(str(x) + " ")
            fr.write("(" + str(len(dict[x])) + ")" + ":" + " ")
            fr.write(",".join([str(i) for i in dict[x]]))
            fr.write("\n")
        fr.write("\n")


f = open("output.txt", "a")
f.write(", ".join(tokens))
f.close()
