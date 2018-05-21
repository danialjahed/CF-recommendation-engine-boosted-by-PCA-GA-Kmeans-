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

# from collections import OrderedDict as od

##################################################################################
# Data
##################################################################################
# Load movie names and movie ratings
# movies = pd.read_csv('movies.csv',encoding='latin-1')
# ratings = pd.read_csv('ratings.csv')
# ratings.drop(['timestamp' ], axis=1, inplace=True)
#
# print("data has been loaded")
#
# def replace_name(x):
# 	return movies[movies['movieId']==x].title.values[0]
# ratings.movieId = ratings.movieId.map(replace_name)
#
# M = ratings.pivot_table(index=['userId'], columns=['movieId'], values='rating')
# m = M.shape
#
# print (m)
# print("data has generated")
#
# df1 = M.replace(np.nan, 0, regex=True)
#
# print("data has generated")
#
# df1.to_csv("df1.csv")
#print("df1 saved")

df1 = pd.read_csv("")
df1.drop('userId', axis=1, inplace=True)
X_std = StandardScaler().fit_transform(df1)

##################################################################################
z=500

# dic={}
# for j in df1.columns:
#     dic[j]=0
#
# cols = ["pc-1"]
# for j in range(2,z+1):
#     cols.append("pc-"+str(j))


##################################################################################
# PCA Analysis
##################################################################################
# Create a covariance matrix
# mean_vec = np.mean(X_std, axis=0)
# cov_mat = (X_std - mean_vec).T.dot((X_std - mean_vec)) / (X_std.shape[0]-1)
# print('Covariance matrix \n%s' %cov_mat)
#
# # Create the same covariance matrix with 1 line of code
# print('NumPy covariance matrix: \n%s' %np.cov(X_std.T))
#
# # Perform eigendecomposition on covariance matrix
# cov_mat = np.cov(X_std.T)
# eig_vals, eig_vecs = np.linalg.eig(cov_mat)
# print('Eigenvectors \n%s' %eig_vecs)
# print('\nEigenvalues \n%s' %eig_vals)
#
# # Visually confirm that the list is correctly sorted by decreasing eigenvalues
# eig_pairs = [(np.abs(eig_vals[i]), eig_vecs[:,i]) for i in range(len(eig_vals))]
# print('Eigenvalues in descending order:')
# for i in eig_pairs:
#     print(i[0])
#

pca = PCA(n_components=z)
result = pca.fit_transform(X_std)
result = pd.DataFrame(result)
result.to_csv("PCA_Y_result_n500.csv")

#########################
# i = np.identity(df1.shape[1])
# coef = pca.transform(i)
#########################
# coef = np.copy(pca.components_)
# coef = np.copy(coef.T)
#########################
# coef_abs=np.abs(coef)
# loadings = pd.DataFrame(coef_abs,columns=cols, index=df1.columns)
# #print (loadings.head(10))
# for j in range(1,z):
#     loadings = loadings.sort(columns=("pc-"+str(j)),ascending=0)
#     dic[loadings.first_valid_index()] +=1;
#     # print(dic[loadings.first_valid_index()])
# r = sorted(dic.items(), key=op.itemgetter(1),reverse=True)
# r = np.array(r)
# r = pd.DataFrame(r)
# r.to_csv("test_2500_withPCAComponentes.csv")

print("#######################################################")

#print the eigenvalues for the first two principle components
# print (np.cumsum(pca.explained_variance_ratio_))

#Explained variance
# pca = PCA().fit(X_std)
# plt.plot(np.cumsum(pca.explained_variance_ratio_))
# plt.xlabel('number of components')
# plt.ylabel('cumulative explained variance')
# plt.show()