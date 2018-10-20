from nltk.corpus import stopwords
from stemming.porter2 import stem
import nltk

word = "happy"
word = stem(word)

print (word)
