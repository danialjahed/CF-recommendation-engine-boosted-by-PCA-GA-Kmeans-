import numpy as np
import pandas as pd
import os
import math
##################load data

data_Nan = pd.read_csv("original_Scaled(11)_NAN.csv")
data_Nan.drop(data_Nan.columns[0],axis=1,inplace=True)


test = data_Nan.iloc[0:math.ceil (data_Nan.shape[0]/10),:]
train =data_Nan.iloc[math.ceil (data_Nan.shape[0]/10):,:]

test.to_csv("test_Scaled.csv")
train.to_csv("train_Scaled.csv")