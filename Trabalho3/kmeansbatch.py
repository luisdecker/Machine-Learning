
# coding: utf-8

# In[ ]:


import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from docOps import Document
from sklearn.neighbors import NearestNeighbors


# In[ ]:


class KMeans_Batch:
    
    def __init__(self,data,init_method,num_inits,iterations,km_algorithm,docs):
        #Configurações globais
        self.raw_data = data
        self.init_method = init_method
        self.num_inits = num_inits
        self.iterations = iterations
        self.km_algorithm = km_algorithm
        self.docs = docs
        
    def knn(self,k,point):
        neigh = NearestNeighbors(n_neighbors=k,algorithm = 'ball_tree')
        neigh.fit(self.raw_data)
        return neigh.kneighbors(point.reshape(1,-1),return_distance=False)
      
    def run(self,k):
        #Treinamos o k-means
        kmeans = KMeans(
            n_clusters=k,
            n_jobs=-1,
            init=self.init_method,
            n_init=self.num_inits,
            precompute_distances=True,
            max_iter=self.iterations,
            algorithm=self.km_algorithm)
        kmeans.fit(self.raw_data)
        #Separamos os documentos por classes
        doc_classes = {}
        file_index=0
        for cluster in kmeans.labels_:
            if cluster not in doc_classes.keys():
                doc_classes[cluster] = []
            doc_classes[cluster].append(self.docs[file_index])
            file_index += 1
        #Verificamos os 10 vizinhos mais próximos de cada centroide
        centroids_knn = {}
        centroids = kmeans.cluster_centers_
        for cluster in range(k):
            centroids_knn[cluster] = self.knn(10,centroids[cluster])
        
        #Salvamos o resultado num arquivo
        #Iremos salvar o Newsgroups dos 10nn de cada 
        results = open(file="ResultsKnn"+str(k)+".txt",mode='w')
        #print(centroids_knn)
        for cluster in range(k):
            ten_nn = centroids_knn[cluster] #indice dos 10nn
            ten_nn = ten_nn[0]

            
      
           
            print("\n\n================================================================================\n",file=results)
            print("CLUSTER {}".format(cluster),file=results)
            print("Medoid:",file=results)
            print(self.docs[(ten_nn[0])].groups,file=results)
            print("10nn:",file=results)
           
            for point in (ten_nn):
                index = point
                if index == -1:
                    print ("Não achou um dado!")
                classes = self.docs[index].groups
                print(classes,file=results)
            
            print ("\n______ALL______\n",file=results)
            all_groups = set()
            for doc in doc_classes[cluster]:
                all_groups = all_groups.union(doc.groups)
            print(all_groups,file=results)


