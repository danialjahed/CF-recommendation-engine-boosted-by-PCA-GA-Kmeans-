import os
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
import pickle as pk

data = pd.read_csv("PCA_Y_result_n63.csv")
data.drop([data.columns[0]], axis=1, inplace=True)

GA_centers = pd.read_csv("GA_20.csv")
GA_centers.drop(GA_centers.columns[0],axis=1,inplace=True)

model = KMeans(n_clusters=20, max_iter=600,init=GA_centers.as_matrix(),n_init=1)
model.fit(data)

labels = pd.DataFrame(model.labels_)
labels.to_csv("labels.csv")

output = open('Kmeans.pkl', 'wb')
pk.dump(model, output)