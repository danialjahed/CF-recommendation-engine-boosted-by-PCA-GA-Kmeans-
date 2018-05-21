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


path_ID = "K-fold/K-fold_based on movie ID/"
# path_name = "K-fold/K-fold_based on movie name/"
K=10
z = 2500
# num_components=[2500,]
for i in range(0,K):

    df1 = pd.read_csv(path_ID+str(i)+"/train.csv")
    df1.drop([df1.columns[0]], axis=1, inplace=True)
    X_std = StandardScaler().fit_transform(df1)


    pca = PCA(n_components=z)
    result = pca.fit_transform(X_std)
    result = pd.DataFrame(result)
    result.to_csv(path_ID+str(i)+"/PCA_Y_result_n" + str(z) + "_with_movieID.csv")

    plt.plot(np.cumsum(pca.explained_variance_ratio_))
    plt.xlabel('number of components')
    plt.ylabel('cumulative explained variance')
    plt.savefig(path_ID+str(i)+"/PCA_Y_result_n" + str(z) + "_with_movieID.png")

    output = open(path_ID+str(i)+'/PCA_object.pkl', 'wb')
    pk.dump(pca, output)


    # pca = PCA()
    # result = pca.fit_transform(X_std)
    # result = pd.DataFrame(result)
    # result.to_csv(path_ID+str(i)+"/PCA_Y_result_nComplete_with_movieID.csv")
    #
    # plt.plot(np.cumsum(pca.explained_variance_ratio_))
    # plt.xlabel('number of components')
    # plt.ylabel('cumulative explained variance')
    # plt.savefig(path_ID+str(i)+"/PCA_Y_result_nComplete_with_movieID.png")


    ###################################


    # df1 = pd.read_csv(path_name + str(i) + "/train.csv")
    # df1.drop([df1.columns[0]], axis=1, inplace=True)
    # X_std = StandardScaler().fit_transform(df1)
    #
    # pca = PCA(n_components=z)
    # result = pca.fit_transform(X_std)
    # result = pd.DataFrame(result)
    # result.to_csv(path_name + str(i) +"/PCA_Y_result_n" + str(z) + "_with_movieName.csv")
    #
    # plt.plot(np.cumsum(pca.explained_variance_ratio_))
    # plt.xlabel('number of components')
    # plt.ylabel('cumulative explained variance')
    # plt.savefig(path_name + str(i) +"/PCA_Y_result_n" + str(z) + "_with_movieName.png")
    #
    #
    # pca = PCA()
    # result = pca.fit_transform(X_std)
    # result = pd.DataFrame(result)
    # result.to_csv(path_name + str(i) +"/PCA_Y_result_nComplete_with_movieName.csv")
    #
    # plt.plot(np.cumsum(pca.explained_variance_ratio_))
    # plt.xlabel('number of components')
    # plt.ylabel('cumulative explained variance')
    # plt.savefig(path_name + str(i) +"/PCA_Y_result_nComplete_with_movieName.png")

