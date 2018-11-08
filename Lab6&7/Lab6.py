from nltk.corpus import stopwords
from stemming.porter2 import stem
import nltk

tokens = []

with open("tweetsclassification/Tweets.14cat.train") as fp:
    for line in fp:
        token = line.split("\t")
        print(token)

'''tokens = nltk.word_tokenize(file_content)
tokens = [token.lower() for token in tokens if token.isalpha() and token not in stopwords.words('english')]
#tokens = [stem(token) for token in tokens]
tokens = [token for token in tokens if token != "id" and token != "text"]
output = set(tokens)
tokens = list(output)'''
