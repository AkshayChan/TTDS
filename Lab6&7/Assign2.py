
#This dictionary has each of the system numbers as the keys with the query numbers again as keys and the document number, rank and score as the value
#Example - {1:{1:[6567,1,5.0743]}}
dictir = {}

#This dictionary has each of the query numbers as keys with the document numbers and relevance as key value pairs
#Example - {1:{9090 :3}}
retr = {}

#Reading all the files at once
for i in range(1, 7):
    filename = "systems/S" + str(i) + ".results"
    with open(filename) as fp:
        for line in fp:
            tokens = line.split(" ")
            #If the system number is already not in
            if i not in dictir:
                dictir.update({i: {tokens[0] : [tokens[2], tokens[3], tokens[4]]}})
            else:
                dictir[i].update({tokens[0] : [tokens[2], tokens[3], tokens[4]]})

print(dictir)
