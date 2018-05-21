import math
import os
import numpy as np
import pandas as pd
import pickle as pk

Y = pd.read_csv("K-fold/K-fold_based on movie ID/0/PCA_Y_result_n2500_with_movieID.csv")
Y.drop([Y.columns[0]], axis=1, inplace=True)

# print(Y.head())
labels = pd.read_csv("K-fold/K-fold_based on movie ID/0/K-means/k-50/labels.csv")
labels.drop([labels.columns[0]], axis=1, inplace=True)

Y = Y.as_matrix()
labels = labels.as_matrix()

pkl_file = open('K-fold/K-fold_based on movie ID/0/K-means/k-50/Kmeans.pkl', 'rb')

model = pk.load(pkl_file)


l = []
for i in range(0,len(Y)):
    # min_dist = 99999999999999999999999999999
    # best_cluster = 0
    # for j in range(0,len(Cen)):
    #     r = np.linalg.norm(Y[i]-Cen[j])
    #     if r < min_dist:
    #         best_cluster = j
    #         min_dist = r
    #
    best_cluster = model.predict(Y[i])[0]
    l.append([best_cluster,labels[i],best_cluster==labels[i]])
    # print()

l = pd.DataFrame(l,columns=["best_cluster","real_label","diff"])
l.to_csv("predict_lables.csv")


