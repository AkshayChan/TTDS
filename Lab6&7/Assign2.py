import operator
import math

#This dictionary has each of the system numbers as the keys with the query numbers again as keys and the rank again as a key
#With the doc number and score as a list of values
#Example - {1:{1:{1:[6567,5.0743]}}}
dictir = {}

#This dictionary has each of the query numbers as keys with the document numbers and relevance as key value pairs
#Example - {1:{9090 :3}}
retr = {}
sorted_retr = {}

#System numbers are ints, query numbers are ints, ranks are ints and scores are floats

#Reading all the files at once
for i in range(1, 7):
    filename = "systems/S" + str(i) + ".results"
    with open(filename) as fp:
        for line in fp:
            tokens = line.split(" ")
            #If we already have the system number in our dictionary
            if i in dictir:
                #If we already have the query number in our inner (2nd level) dictionary
                if int(tokens[0]) in dictir[i]:
                    #Upper the innermost (3rd level) dictionary
                    dictir[i][int(tokens[0])].update({int(tokens[3]): [int(tokens[2]), float(tokens[4])]})
                #Update the inner (2nd level) dictionary - adding the query number
                else:
                    dictir[i].update({int(tokens[0]): {int(tokens[3]): [int(tokens[2]), float(tokens[4])]}})
            #Update the dictionary - adding the system number
            else:
                dictir.update({i: {int(tokens[0]): {int(tokens[3]): [int(tokens[2]), float(tokens[4])]}}})
#print(dictir)

#query numbers are int, document numbers are int and the relevance is also an integer

with open("systems/qrels.txt") as fr:
    for line in fr:
        #Split the line on spaces first
        tokens = line.split()
        #Get the query number first
        qno = int(tokens[0].split(":")[0])

        #Take out the query number from the list now
        tokens.remove(tokens[0])
        for token in tokens:
            #Get the document numbers and relevance value
            qtok = token.split(",")
            docno = int(qtok[0].replace('(', ""))
            rele = int(qtok[1].rstrip().replace(')', ""))

            #If we already have the query number in our dictionary
            if qno in retr:
                retr[qno].update({docno: rele})
            else:
                retr.update({qno: {docno: rele}})
#print(retr)

#Each system
for i in dictir:

    filename = "S" + str(i) + ".eval"
    fq = open(filename, "a")
    fq.write("        ")
    fq.write("P@10")
    fq.write("    ")
    fq.write("R@50")
    fq.write("    ")
    fq.write("r-Precision")
    fq.write("    ")
    fq.write("AP")
    fq.write("    ")
    fq.write("nDCG@10")
    fq.write("    ")
    fq.write("nDCG@20")
    fq.write("\n")

    #Each query
    for j in dictir[i]:

        #Formatting of the file
        if (j == 10):
            fq.write(str(j))
            fq.write("      ")
        else:
            fq.write(str(j))
            fq.write("       ")


        #Precision at 10
        precsum = 0
        for k in range(1, 11):
            #If the document number is in the list of relevant documents for the query
            if dictir[i][j][k][0] in retr[j]:
                precsum = precsum + 1
        #What fraction of the retrieved documents are relevant?
        precsum = format(precsum/10.0, '.2f')
        fq.write(str(precsum))
        fq.write("    ")


        #Recall at 50
        recsum = 0
        for k in range(1, 51):
            #If the document number is in the list of relevant documents for the query
            if dictir[i][j][k][0] in retr[j]:
                recsum = recsum + 1
        #What fraction of the relevant documents are retrieved?
        recsum = round(float(recsum)/len(retr[j]), 2)
        recsum = format(recsum, '.2f')
        fq.write(str(recsum))
        fq.write("    ")


        #R - Precision
        rpsum = 0
        #length of the dictionary, number of relevant documents for each query
        rpindex = len(retr[j])
        for k in range(1, rpindex + 1):
            #If the document number is in the list of relevant documents for the query
            if dictir[i][j][k][0] in retr[j]:
                rpsum = rpsum + 1
        #What fraction of the retrieved documents are relevant?
        rpsum = format(float(rpsum)/rpindex, '.2f')
        fq.write(str(rpsum))
        fq.write("           ")


        #Average Precision
        #To count the number of retrieved documents yet
        retcounter = 0
        avgsum = 0
        #Over all the results for a given system and query
        for k in dictir[i][j]:
            if dictir[i][j][k][0] in retr[j]:
                #Update the counter first
                retcounter = retcounter + 1
                #Number of the relevant doc retrieved/total docs retrieved yet
                avgsum = avgsum + (float(retcounter)/k)
        #Divide by the total number of  relevant docs retrieved
        if (retcounter == 0):
            avgsum = 0.00
            avgsum = format(avgsum, '.2f')
        else:
            avgsum = avgsum/retcounter
            avgsum = round(avgsum, 2)
            avgsum = format(avgsum, '.2f')
        fq.write(str(avgsum))
        fq.write("    ")

        #We have to sort out retr dictionary of related documents for queries to get the ideal gain at every step
        for x in retr:
            sorted_retr[x] = sorted(retr[x].items(), key=operator.itemgetter(1), reverse = True)
        #print(sorted_retr)

        #nDCG@10
        #For getting the ID gain
        counter = 0
        dcg = 0
        idcg = 0
        for k in range(1, 11):

            #i,j,k are system, query and rank
            docID = dictir[i][j][k][0]
            if docID in retr[j]:
                #Gain is the releavnce of that specific document
                gain = retr[j][docID]
            else:
                #Else relevance is 0 if the document is not relevant
                gain = 0.0

            #The first gain value in  the sorted list
            #Only if the we have not covered all the relevant documents
            if (counter >= len(sorted_retr[j])):
                id_gain = 0.0
            else:
                id_gain = sorted_retr[j][counter][1]

            counter = counter + 1
            if k == 1:
                #We simply add the gain for the first one
                dcg = dcg + gain
                idcg = idcg + id_gain
            else:
                #We do the log of the rank too
                dcg = dcg + (float(gain)/math.log(k, 2.0))
                idcg = idcg + (float(id_gain)/math.log(k, 2.0))
        ndcg = round(dcg/idcg, 2)
        ndcg = format(ndcg, '.2f')
        fq.write(str(ndcg))
        fq.write("    ")

        #nDCG@20
        #For getting the ID gain
        counter = 0
        dcg = 0
        idcg = 0
        for k in range(1, 21):

            #i,j,k are system, query and rank
            docID = dictir[i][j][k][0]
            if docID in retr[j]:
                #Gain is the releavnce of that specific document
                gain = retr[j][docID]
            else:
                #Else relevance is 0
                gain = 0.0

            #The first gain value in  the sorted list
            #Only if the we have not covered all the relevant documents
            if (counter >= len(sorted_retr[j])):
                id_gain = 0.0
            else:
                id_gain = sorted_retr[j][counter][1]

            counter = counter + 1
            if k == 1:
                #We simply add the gain
                dcg = dcg + gain
                idcg = idcg + id_gain
            else:
                #We do the log of the rank too
                dcg = dcg + (float(gain)/math.log(k, 2.0))
                idcg = idcg + (float(id_gain)/math.log(k, 2.0))
        ndcg = round(dcg/idcg, 2)
        ndcg = format(ndcg, '.2f')
        fq.write(str(ndcg))
        fq.write("    ")
        fq.write("\n")
