import os
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
import pickle as pk

K_fold=10

LowerBond = 20
HigherBond = 75
Step = 5

path = "K-fold/K-fold_based on movie ID/"

for j in range(0,K_fold):

    _path = path+str(j)
    data = pd.read_csv(_path+"/PCA_Y_result_n2500_with_movieID.csv")
    data.drop([data.columns[0]], axis=1, inplace=True)

    _path += "/K-means/"
    if not os.path.exists(_path):
        os.makedirs(_path)


    for i in range(LowerBond,HigherBond+Step,Step):
        print("("+str(j)+","+str(i)+")")
        GA_centers = pd.read_csv("Genetic_Result/"+str(i)+"/"+str(i)+".csv")

        model = KMeans(n_clusters=i, max_iter=600,init=GA_centers.as_matrix(),n_init=1)
        model.fit(data)

        if not os.path.exists(_path+"k-"+str(i)):
            os.makedirs(_path+"k-"+str(i))

        labels = pd.DataFrame(model.labels_)
        labels.to_csv(_path+"k-"+str(i)+"/labels.csv")
        labels.to_json(_path + "k-" + str(i) + "/labels(index).json", orient="index")
        labels.to_json(_path + "k-" + str(i) + "/labels(split).json", orient="split")
        labels.to_json(_path + "k-" + str(i) + "/labels(records).json", orient="records")
        labels.to_json(_path + "k-" + str(i) + "/labels(values).json", orient="values")


        centroids = pd.DataFrame(model.cluster_centers_)
        centroids.to_csv(_path+"k-"+str(i)+"/centroids.csv")
        centroids.to_json(_path + "k-" + str(i) + "/centroids.json",orient="index")

        output = open(_path+"k-"+str(i)+'/Kmeans.pkl', 'wb')
        pk.dump(model, output)