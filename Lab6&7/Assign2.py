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
    fq.write("\t")
    fq.write("P@10")
    fq.write("\t")
    fq.write("R@50")
    fq.write("\t")
    fq.write("r-Precision")
    fq.write("\t")
    fq.write("AP")
    fq.write("\t")
    fq.write("nDCG@10")
    fq.write("\t")
    fq.write("nDCG@20")
    fq.write("\n")

    meanp10 = 0.0
    meanr50 = 0.0
    meanrp = 0.0
    meanap = 0.0
    meandc10 = 0.0
    meandc20 = 0.0

    #Each query
    for j in dictir[i]:

        #Formatting of the file
        if (j == 10):
            fq.write(str(j))
            fq.write("\t")
        else:
            fq.write(str(j))
            fq.write("\t")


        #Precision at 10
        precsum = 0
        for k in range(1, 11):
            #If the document number is in the list of relevant documents for the query
            if dictir[i][j][k][0] in retr[j]:
                precsum = precsum + 1
        #What fraction of the retrieved documents are relevant?
        meanp10 = meanp10 + precsum/10.0
        precsum = format(precsum/10.0, '.3f')
        fq.write(str(precsum))
        fq.write("\t")


        #Recall at 50
        recsum = 0
        for k in range(1, 51):
            #If the document number is in the list of relevant documents for the query
            if dictir[i][j][k][0] in retr[j]:
                recsum = recsum + 1
        #What fraction of the relevant documents are retrieved?
        meanr50 = meanr50 + float(recsum)/len(retr[j])
        recsum = round(float(recsum)/len(retr[j]), 3)
        recsum = format(recsum, '.3f')
        fq.write(str(recsum))
        fq.write("\t")


        #R - Precision
        rpsum = 0
        #length of the dictionary, number of relevant documents for each query
        rpindex = len(retr[j])
        for k in range(1, rpindex + 1):
            #If the document number is in the list of relevant documents for the query
            if dictir[i][j][k][0] in retr[j]:
                rpsum = rpsum + 1
        #What fraction of the retrieved documents are relevant?
        meanrp = meanrp + float(rpsum)/rpindex
        rpsum = format(float(rpsum)/rpindex, '.3f')
        fq.write(str(rpsum))
        fq.write("\t")


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
            meanap = meanap + avgsum
            avgsum = format(avgsum, '.3f')
        else:
            avgsum = avgsum/retcounter
            meanap = meanap + avgsum
            avgsum = round(avgsum, 3)
            avgsum = format(avgsum, '.3f')
        fq.write(str(avgsum))
        fq.write("\t")

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
        ndcg = round(dcg/idcg, 3)
        meandc10 = meandc10 + ndcg
        ndcg = format(ndcg, '.3f')
        fq.write(str(ndcg))
        fq.write("\t")

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
        ndcg = round(dcg/idcg, 3)
        meandc20 = meandc20 + ndcg
        ndcg = format(ndcg, '.3f')
        fq.write(str(ndcg))
        fq.write("\n")

    #Now we write the means here
    fq.write("mean")
    fq.write("\t")

    #Average each mean by the number of queries and round them
    meanp10 = meanp10/len(dictir[i])
    meanp10 = round(meanp10, 3)
    meanp10 = format(meanp10, '.3f')
    meanr50 = meanr50/len(dictir[i])
    meanr50 = round(meanr50, 3)
    meanr50 = format(meanr50, '.3f')
    meanrp = meanrp/len(dictir[i])
    meanrp = round(meanrp, 3)
    meanrp = format(meanrp, '.3f')
    meanap = meanap/len(dictir[i])
    meanap = round(meanap, 3)
    meanap = format(meanap, '.3f')
    meandc10 = meandc10/len(dictir[i])
    meandc10 = round(meandc10, 3)
    meandc10 = format(meandc10, '.3f')
    meandc20 = meandc20/len(dictir[i])
    meandc20 = round(meandc20, 3)
    meandc20 = format(meandc20, '.3f')

    #Now we write all of the means to the files
    fq.write(str(meanp10))
    fq.write("\t")
    fq.write(str(meanr50))
    fq.write("\t")
    fq.write(str(meanrp))
    fq.write("\t")
    fq.write(str(meanap))
    fq.write("\t")
    fq.write(str(meandc10))
    fq.write("\t")
    fq.write(str(meandc20))
