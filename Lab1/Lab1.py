
#from nltk.tokenize import word_tokenize
#with open ('pg10.txt') as fin, open('output.txt', "a") as fout:
    #tokens = word_tokenize(line)
    #fout.write("\n".join(tokens))

from nltk.corpus import stopwords
from stemming.porter2 import stem
import nltk
file_content = open("pg10.txt").read()
tokens = nltk.word_tokenize(file_content)
tokens = [token.lower() for token in tokens if token.isalpha() and token not in stopwords.words('english')]
tokens = [stem(token) for token in tokens]
f = open("output.txt", "a")
f.write("\n".join(tokens))
f.close()
