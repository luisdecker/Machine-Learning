import os

class Document:
    def __init__(self,path=""):
        if not path == "":
            self.name = os.path.splitext(os.path.basename(path))[0]
            file = open(path).readlines()
            for line in file:
                if line.startswith("Newsgroups:"):
                    groups = line[len("Newsgroups: "):].split(',')
                    self.groups = [group.strip() for group in groups]
                    break

                    
           