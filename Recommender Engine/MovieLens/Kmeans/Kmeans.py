import os
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans

# data = pd.read_csv("Input Data/PCA_Y_result_nCompelte(3706).csv")
# data = pd.read_csv("Input Data/PCA_Y_result_n2500.csv")
data = pd.read_csv("Input Data/X_original_complete_NAN.csv")

data.drop([data.columns[0]], axis=1, inplace=True)
data = data.as_matrix()
data = np.copy(data)

lower_bond=25
higher_bond = 171

for k in range(lower_bond,higher_bond):
    model = KMeans(n_clusters=k,max_iter=600)
    model.fit(data)

    path = "Output Data/X_NAN_noGA"+"/k-"+str(k)+"/"

    if not os.path.exists(path):
        os.makedirs(path)

    labels = model.labels_
    labels = np.copy(labels)
    labels = pd.DataFrame(labels)
    labels.to_csv(path+"labels.csv")

    centroids = model.cluster_centers_
    centroids = np.copy(centroids)
    centroids = np.copy(centroids)
    centroids = pd.DataFrame(centroids)
    centroids.to_csv(path+"centroids.csv")