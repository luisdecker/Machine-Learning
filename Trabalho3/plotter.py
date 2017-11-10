
# coding: utf-8

# In[6]:


import os
import matplotlib.pyplot as plt


# In[8]:


class plotter:
    def plot_graph(dataX,dataY,labelX,labelY,title):
        plt.rcParams["figure.figsize"] = (10,5)
        plt.plot(dataX, dataY, 'bx-')
        plt.xlabel(labelX)
        plt.ylabel(labelY)
        plt.title(title)
        plt.show()
    def plot_silhouette(K,silhouette):
        plotter.plot_graph(K,silhouette,"K","Silhueta","Coeficiente de Silhueta")


