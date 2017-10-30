import os

i=0
for filename in os.listdir("documents/test"):
    #print("Document {}: [{}]".format(i,filename))
    i=i+1;
    
    #Open document
    file = open("documents/docs/{}".format(filename))
    fileLines = file.readlines()
    print ("File {} with {} lines".format(i,len(fileLines)))
    for line in fileLines:
        if(line.startswith("Newsgroups:")):
            print(line)
