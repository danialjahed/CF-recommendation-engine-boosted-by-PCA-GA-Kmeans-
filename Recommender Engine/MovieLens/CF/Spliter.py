import os
import numpy as np
import pandas as pd

X_NAN = pd.read_csv("X_original_complete_NAN.csv")
X_NAN.drop([X_NAN.columns[0]],axis=1,inplace=True)

labels = pd.read_csv("labels.csv")
labels.drop([labels.columns[0]],axis=1,inplace=True)
labels = labels.as_matrix()

users = []
X_NAN_path = "Splited Data/"

if not os.path.exists(X_NAN_path):
    os.makedirs(X_NAN_path)


for i in range(0,20):
    for j in range(0,X_NAN.shape[0]):
        if labels[j]==i:
            users.append(j)

    data = X_NAN.ix[users]
    data = pd.DataFrame(data)
    data.to_csv(X_NAN_path+str(i)+".csv")

    users.clear()