from nltk.corpus import stopwords
from stemming.porter2 import stem
import nltk

stopwordsli = []

with open ("CW1collection/stopwords.txt") as fil:

    for lines in fil:
        stopwordsli.append(lines.rstrip())

    print(stopwordsli)
