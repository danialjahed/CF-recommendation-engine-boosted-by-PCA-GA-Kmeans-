import math
import os
import numpy as np
import pandas as pd
import multiprocessing as pool
from multiprocessing import Manager
import pickle as pk
import pymongo
import sys
import os.path
from operator import itemgetter
#data base config
client = pymongo.MongoClient("localhost", 27017)
db = client.movie_db

def Dot(iterator,k,l,R,u,start,end,return_value):
    result = []
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
            q = (R+(m/n))
            result.append([u.index[a],u[u.index[a]],q,abs((q-u[a]))])
        else:
            result.append([u.index[a],u[u.index[a]],np.nan,np.nan])
    return_value[iterator] = result


#   load StandardScaler object
scriptpath = os.path.dirname(__file__)+'/'
pkl_file = open(scriptpath+'StandardScaler_object.pkl', 'rb')
Standarder = pk.load(pkl_file)

#   load PCA object
pkl_file = open(scriptpath+'PCA_object.pkl', 'rb')
pca = pk.load(pkl_file)

#   load k-means object
pkl_file = open(scriptpath+'Kmeans.pkl', 'rb')
clustring_model = pk.load(pkl_file)

################this sction must be delete################

#   load test dataset
X_NAN_ALL = pd.read_csv(scriptpath+"X_original_complete_NAN.csv")
X_NAN_ALL.drop([X_NAN_ALL.columns[0]], axis=1, inplace=True)
#   select user
i=10
user_data = db.rates.aggregate(
    [{
        "$match": {
            "$or": [{
                "user_id": str(sys.argv[1])
            }]
        }
    }, {
        "$project": {
            "_id": 0,
            'movie_id': "$movie_rate.movie_id",
            'rate': "$movie_rate.rate"
        }
    }])


#   get user i from X_NAN_ALL
user_data = list(user_data)
data = pd.Series(user_data[0]['rate'],index=user_data[0]['movie_id'])
U = data.fillna(np.nan)

##########################################################

#   give user i to PCA
X_std = Standarder.transform(U.fillna(0))
Y_U = pca.transform(X_std)

#   give PCA output to k-mean predict
U_cluster_num = clustring_model.predict(Y_U[0])



#   load cluster based on k-means predict output
X_NAN = pd.read_csv(scriptpath+"Splited Data/" + str(U_cluster_num[0]) + ".csv")
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
p1 = pool.Process(target=Dot, args=(1, Sim, predict_rates, R_mean, U, 0, 800, return_value))
p1.start()
jobs.append(p1)
p2 = pool.Process(target=Dot, args=(2, Sim, predict_rates, R_mean, U, 800, 1600, return_value))
p2.start()
jobs.append(p2)
p3 = pool.Process(target=Dot, args=(3, Sim, predict_rates, R_mean, U, 1600, 2400, return_value))
p3.start()
jobs.append(p3)
p4 = pool.Process(target=Dot, args=(4, Sim, predict_rates, R_mean, U, 2400, len(predict_rates[0]), return_value))
p4.start()
jobs.append(p4)
for proc in jobs:
    proc.join()

#   sort output and find out recommendation

ll = return_value[1]+return_value[2]+return_value[3]+return_value[4]
#

p = pd.DataFrame(ll,  columns=["MovieID","User_rate", "predict_rates", "diff"])
# p.to_csv("predict_rates.csv")
#
# mean_var = []
# mean_var.append([np.nanmean(p.ix[:,"diff"]),np.nanvar(p.ix[:,"diff"])])
#
# mv = pd.DataFrame(mean_var,columns=["mean","var"])
# mv.to_csv("mean_var.csv")
#
p_sorted = p.sort(columns=["predict_rates"], ascending=0)
print(p_sorted.iloc[0,:])

recom_film_id = []
cntr = 0
n = 0
while n != 30:
    film_info = p_sorted.iloc[cntr,:]
    if np.isnan(film_info[1]):
        recom_film_id.append(film_info[0])
        n +=1
    cntr += 1

db.rates.update({
   "user_id": str(sys.argv[1])
}, {
   "$set": {
       "recom_movie": recom_film_id
   }
})
print("Done")
# print(recom_film_id)
# pd.DataFrame(recom_film_id).to_csv("recom_film_id.csv")
