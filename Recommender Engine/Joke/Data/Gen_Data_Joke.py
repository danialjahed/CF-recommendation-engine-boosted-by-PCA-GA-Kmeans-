import pandas as pd
import numpy as np
import operator as op



data = pd.read_csv("original_NAN.csv")

data.drop(data.columns[0], axis=1, inplace=True)

print("data has been loaded")



for i in range(0,data.shape[0]):
    for j in range(0,data.shape[1]):
        data.iloc[i, j] += 11


data.to_csv("original_Scaled(11)_NAN.csv")