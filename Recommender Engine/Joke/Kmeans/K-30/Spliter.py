import os
import numpy as np
import pandas as pd

X_NAN = pd.read_csv("train_Scaled.csv")
X_NAN.drop([X_NAN.columns[0]],axis=1,inplace=True)

users = []

write_path = "Splited Data/k-30/"
if not os.path.exists(write_path):
    os.makedirs(write_path)


labels = pd.read_csv("labels.csv")
labels.drop([labels.columns[0]], axis=1, inplace=True)
labels = labels.as_matrix()

for i in range(0,30):
    for j in range(0,X_NAN.shape[0]):
        if labels[j]==i:
            users.append(j)

    data = X_NAN.ix[users]
    data = pd.DataFrame(data)

    data.to_csv(write_path+str(i)+".csv")
    users.clear()

