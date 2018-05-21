import numpy as pd
import pandas as pd
import os
import math
data_Zero = pd.read_csv("Generated-DataTable/based on movie ID/X_original_complete.csv")
data_Zero.drop([data_Zero.columns[0]], axis=1, inplace=True)

data_Nan = pd.read_csv("Generated-DataTable/based on movie ID/X_original_complete_NAN.csv")
data_Nan.drop([data_Nan.columns[0]], axis=1, inplace=True)


splited_Zero =[]
splited_Nan = []

K = 10
# print(data_Nan.shape[0])
for i in range(1,K+1):#todo:eslahe in ghesmat baraye kar kardan ba K haye mokhtalef
    if (i-1) != 0:
        splited_Zero.append(data_Zero.iloc[math.ceil((i-1) * (data_Zero.shape[0]/10)) : math.ceil(i * (data_Zero.shape[0]/10)), :])
        splited_Nan.append(data_Nan.iloc[math.ceil((i-1) * (data_Nan.shape[0]/10)) : math.ceil(i * (data_Nan.shape[0]/10)),:])
    else:
        splited_Zero.append(data_Zero.iloc[0:math.ceil(data_Zero.shape[0]/10),:])
        splited_Nan.append(data_Nan.iloc[0:math.ceil(data_Nan.shape[0]/10), :])

path = "K-fold/K-fold_based on movie ID/"
if not os.path.exists(path):
    os.makedirs(path)

for i in range(0,K):
    print(i)
    if not os.path.exists(path+str(i)):
        os.makedirs(path+str(i))

    splited_Zero[i].to_csv(path+str(i)+"/test.csv")
    if i == 0:
        out = splited_Zero[1]
        for j in range(2, K):
            if j != i:
                out = out.append(splited_Zero[j])
    else:
        out = splited_Zero[0]
        for j in range(1, K):
            if j != i:
                out = out.append(splited_Zero[j])
    out.to_csv(path+str(i)+"/train.csv")


    splited_Nan[i].to_csv(path+str(i)+"/test_Nan.csv")
    if i == 0:
        out = splited_Nan[1]
        for j in range(2, K):
            if j != i:
                out = out.append(splited_Nan[j])
    else:
        out = splited_Nan[0]
        for j in range(1, K):
            if j != i:
                out = out.append(splited_Nan[j])
    out.to_csv(path+str(i)+"/train_Nan.csv")