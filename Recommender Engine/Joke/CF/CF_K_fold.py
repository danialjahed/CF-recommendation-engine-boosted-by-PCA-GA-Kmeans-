import math
import os
import numpy as np
import pandas as pd
import multiprocessing as pool
from multiprocessing import Manager
import pickle as pk
from operator import itemgetter


def Dot(iterator,k,l,R,u,start,end,return_value):
    result = []
    allrated = 0
    diffsum = 0
    allpos = 0
    tp = 0
    fn = 0
    fp = 0

    for a in range(start,end):

        m = 0
        n = 0
        for b in range(0,len(k)):
            if not np.isnan(l[b][a]):
                if not np.isnan(k[b]):
                    # m += l[j][i]
                    # n += 1
                    m += k[b]*l[b][a]
                    n += abs(k[b])
        if n != 0:
            q = (R+(m/n)) #### predicted rate
            rate_diff = abs((q-u[a]))
            result.append([a+1,u[a],q,rate_diff])
            ############ for precion & recall & MSE
            if not np.isnan(u[a]) :
                allrated += 1
                diffsum += rate_diff
                if u[a] >= 14:
                    allpos += 1
                    if q >=11:
                        tp += 1
                    else:
                        fn += 1
                else:
                    if q >= 11:
                        fp += 1

        else:
            result.append([a+1,u[a],np.nan,np.nan])
    return_value[iterator] = [result,allrated,diffsum,allpos,tp,fn,fp,math.pow(diffsum,2)]


#   load test dataset
X_NAN_ALL = pd.read_csv("test_Scaled.csv")
X_NAN_ALL.drop([X_NAN_ALL.columns[0]], axis=1, inplace=True)

#   load StandardScaler object
pkl_file = open('StandardScaler_object.pkl', 'rb')
Standarder = pk.load(pkl_file)

#   load PCA object
pkl_file = open('PCA_object.pkl', 'rb')
pca = pk.load(pkl_file)


#   load k-means object
pkl_file = open('Kmeans.pkl', 'rb')
clustring_model = pk.load(pkl_file)

Total_allrated = 0
Total_diffsum = 0
Total_allpos = 0
Total_tp = 0
Total_fn = 0
Total_fp = 0
Total_Sdiffsum = 0

performance = []

for m in range(0,X_NAN_ALL.shape[0]):

    #   get user m-th from X_NAN_ALL
    U = X_NAN_ALL.iloc[m, :]

    #   give user m to PCA
    X_std = Standarder.transform(U.fillna(0))
    Y_U = pca.transform(X_std)

    #   give PCA output to k-mean predict
    U_cluster_num = clustring_model.predict(Y_U[0])


    #   load cluster based on k-means predict output
    X_NAN = pd.read_csv("Splited Data/"+str(U_cluster_num[0]) + ".csv")
    X_NAN.drop([X_NAN.columns[0]], axis=1, inplace=True)
    X_NAN_T = X_NAN.transpose()

    #   calculate corrwith with pandas
    Sim = X_NAN_T.corrwith(U)
    Sim = Sim.as_matrix()

    #   calculate mean of user i rates
    R_mean = np.mean(U)

    #   calculate mean rate of user cluster
    Rates_bar = np.mean(X_NAN, axis=1)
    Rates_bar = Rates_bar.as_matrix()

    #   subtract user rate cluster with mean rate of them
    X_NAN_M = X_NAN.as_matrix()
    predict_rates = np.subtract(X_NAN_M.T, Rates_bar)
    predict_rates = predict_rates.T

    #   use Dot function
    jobs = []
    manager = Manager()
    return_value = manager.dict()
    p1 = pool.Process(target=Dot, args=(1, Sim, predict_rates, R_mean, U, 0, 25, return_value))
    p1.start()
    jobs.append(p1)
    p2 = pool.Process(target=Dot, args=(2, Sim, predict_rates, R_mean, U, 25, 50, return_value))
    p2.start()
    jobs.append(p2)
    p3 = pool.Process(target=Dot, args=(3, Sim, predict_rates, R_mean, U, 50, 75, return_value))
    p3.start()
    jobs.append(p3)
    p4 = pool.Process(target=Dot, args=(4, Sim, predict_rates, R_mean, U, 75, len(predict_rates[0]), return_value))
    p4.start()
    jobs.append(p4)
    for proc in jobs:
        proc.join()

    ll = return_value[1][0] + return_value[2][0] + return_value[3][0] + return_value[4][0]

    p = pd.DataFrame(ll, columns=["MovieID", "User_rate", "predict_rates", "diff"])
    p.to_csv("Predicted_rate/"+str(m)+".csv")

    for o in range(1, 5):
        Total_allrated += return_value[o][1]
        Total_diffsum += return_value[o][2]
        Total_allpos += return_value[o][3]
        Total_tp += return_value[o][4]
        Total_fn += return_value[o][5]
        Total_fp += return_value[o][6]
        Total_Sdiffsum += return_value[o][7]


performance.append(Total_diffsum/Total_allrated)#MAE
performance.append(Total_Sdiffsum/Total_allrated)#MSE
performance.append(math.sqrt(Total_Sdiffsum/Total_allrated))#RMSE
performance.append(Total_tp/Total_allpos)#Recall
performance.append(Total_tp/(Total_tp+Total_fp))#precision
performance.append( (2*performance[3]*performance[4])/(performance[3]+performance[4]) )#F1


pd.DataFrame(performance,index=["MAE","MSE","RMSE","Recall","precision","F1"]).to_csv("performance.csv")










