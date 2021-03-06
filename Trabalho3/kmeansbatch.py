
# coding: utf-8

# In[ ]:


import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from docOps import Document
from sklearn.neighbors import NearestNeighbors
import operator
from multiprocessing import Pool
from sklearn.metrics import silhouette_score


# In[ ]:


class KMeans_Batch:
    
    def __init__(self,data,init_method,num_inits,iterations,km_algorithm,docs,save_results=False):
        #Configurações globais
        self.raw_data = data
        self.init_method = init_method
        self.num_inits = num_inits
        self.iterations = iterations
        self.km_algorithm = km_algorithm
        self.docs = docs
        self.save_results = save_results
        
    def knn(self,k,point):
        neigh = NearestNeighbors(n_neighbors=k,algorithm = 'ball_tree',n_jobs=-1,leaf_size=60)
        neigh.fit(self.raw_data)
        return neigh.kneighbors(point.reshape(1,-1),return_distance=False)
      
    def run(self,k):
        #Treinamos o k-means
        print("Iniciando KMeans [{}]".format(k))
        kmeans = KMeans(
            n_clusters=k,
            n_jobs=-1,
            init=self.init_method,
            n_init=self.num_inits,
            precompute_distances=True,
            max_iter=self.iterations,
            algorithm=self.km_algorithm)
        kmeans.fit(self.raw_data)
        print("Terminado KMeans [{}]".format(k))
        if self.save_results:
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

            print("Iniciando KNN [{}]".format(k))

            args = []
            for cluster in range(k):#Paralelizavel!
                arg = []
                arg.append(10)
                arg.append(centroids[cluster])
                args.append(arg)
            with Pool(4) as p:
                result = p.starmap(self.knn,args)      
            for cluster in range(k):
                centroids_knn[cluster] = result[cluster]


            print("Terminado KNN [{}]".format(k))

            #Salvamos o resultado num arquivo
            #Iremos salvar o Newsgroups dos 10nn de cada 
            results = open(file="ResultsKnn"+str(k)+".txt",mode='w')
            #print(centroids_knn)
            print("Iniciando gravação [{}]".format(k))
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
                all_groups = {}
                for doc in doc_classes[cluster]:
                    for group in doc.groups:
                        if group not in all_groups.keys():
                            all_groups[group] = 0
                        all_groups[group] += 1
                sorted_groups = sorted(all_groups.items(),key=operator.itemgetter(1),reverse=True)
                for group in sorted_groups:
                    print("{} = {}".format(group[0],group[1]),file=results)
            print("Terminado gravação [{}]".format(k))
        #save
        #Calculamos o valor da silhueta
        print("Iniciando cálculo da silhueta [{}]".format(k))
        return silhouette_score(self.raw_data,kmeans.labels_)
        

