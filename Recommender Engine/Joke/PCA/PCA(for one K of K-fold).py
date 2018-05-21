import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from matplotlib import*
import matplotlib.pyplot as plt
from matplotlib.cm import register_cmap
from scipy import stats
#from wpca import PCA
from sklearn.decomposition import PCA as PCA
import seaborn
import operator as op
import pickle as pk

z = 63

df1 = pd.read_csv("train_Scaled.csv")
df1.drop([df1.columns[0]], axis=1, inplace=True)
df1 = df1.fillna(0)

Standarder = StandardScaler()
Standarder = Standarder.fit(df1)

output = open('StandardScaler_object.pkl', 'wb')
pk.dump(Standarder, output)

X_std = Standarder.transform(df1)


pca = PCA(n_components=z)
pca = pca.fit(X_std)

output = open('PCA_object.pkl', 'wb')
pk.dump(pca, output)

result = pca.transform(X_std)
result = pd.DataFrame(result)
result.to_csv("PCA_Y_result_n" + str(z) + ".csv")
#
# plt.plot(np.cumsum(pca.explained_variance_ratio_))
# plt.xlabel('number of components')
# plt.ylabel('cumulative explained variance')
# plt.savefig("Variance_63_component.png")

