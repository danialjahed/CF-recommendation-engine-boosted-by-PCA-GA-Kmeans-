import os
import numpy as np
import pandas as pd

X = pd.read_csv("/home/danial/PycharmProjects/FinalProject/Recommeder Engine/K-means/Input Data/Original_X_complete.csv")
X.drop([X.columns[0]],axis=1,inplace=True)

X_NAN = pd.read_csv("/home/danial/PycharmProjects/FinalProject/Recommeder Engine/K-means/Input Data/X_original_complete_NAN.csv")
X_NAN.drop([X_NAN.columns[0]],axis=1,inplace=True)

labels = pd.read_csv("labels.csv")
labels.drop([labels.columns[0]],axis=1,inplace=True)
labels = labels.as_matrix()

cen = pd.read_csv("centroids.csv")
cen.drop([cen.columns[0]],axis=1,inplace=True)
cen = cen.as_matrix()

Y = pd.read_csv("/home/danial/PycharmProjects/FinalProject/Recommeder Engine/K-means/Input Data/PCA_Y_result_nCompelte(3706).csv")
Y.drop([Y.columns[0]],axis=1,inplace=True)

users = []
X_path = "Splited Data/X/"
X_NAN_path = "Splited Data/X_NAN/"
Y_path = "Splited Data/Y/"

if not os.path.exists(X_path):
    os.makedirs(X_path)
if not os.path.exists(X_NAN_path):
    os.makedirs(X_NAN_path)
if not os.path.exists(Y_path):
    os.makedirs(Y_path)


for i in range(0,len(cen)):
    for j in range(0,len(X.shape[0])):
        if labels[j]==i:
            users.append(j)
    data = X.ix[users]
    data = pd.DataFrame(data)
    data.to_csv(X_path+str(i)+".csv")

    data = X_NAN.ix[users]
    data = pd.DataFrame(data)
    data.to_csv(X_NAN_path+str(i)+".csv")

    data = Y.ix[users]
    data = pd.DataFrame(data)
    data.to_csv(Y_path+str(i)+".csv")


    users.clear()