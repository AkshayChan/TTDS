
with open("preprocess.txt") as fr,  open("CW1collection/queries.boolean.txt") as fq:

    lis = []

    for line in fq:
        queries = line.split(" ", 1)
        lis.append(queries[1].rstrip())
    print (lis)
