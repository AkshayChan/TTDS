
#from nltk.tokenize import word_tokenize
#with open ('pg10.txt') as fin, open('output.txt', "a") as fout:
    #tokens = word_tokenize(line)
    #fout.write("\n".join(tokens))

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

with open("collections/sample.txt") as fp:
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
            linewo = [wo.lower() for wo in linewo if wo.isalpha() and wo != "text"]
            #For each word in each line
            for lineword in linewo:
                #Convert the word to lower first
                lineword = lineword.lower()
                #Word is equal to our word
                if (word == lineword):
                    #if the document index exists in the list
                    doc_index = (lis.index(ele) + 1)
                    word_index = (linewo.index(lineword))
                    if (doc_index not in dict):
                        dict[doc_index] = [word_index]
                    else:
                        dict[doc_index].append(word_index)
        print ("\n")
        sum = 0
        for x in dict:
            sum = sum + len(dict[x])
        print (str(word) + ":" + " " + str(sum))
        print (dict)
    print ("\n")


f = open("output.txt", "a")
f.write(", ".join(tokens))
f.close()
