import pandas as pd
import numpy as np
import operator as op

# from collections import OrderedDict as od

##################################################################################
# Data
##################################################################################
# Load movie names and movie ratings
movies = pd.read_csv('OriginalData/movies.csv',encoding='latin-1')
# print(movies.shape)
ratings = pd.read_csv('OriginalData/ratings.csv')
ratings.drop(['timestamp' ], axis=1, inplace=True)

print("data has been loaded")

###this section replace movieID with movie name
# def replace_name(x):
# 	return movies[movies['movieId']==x].title.values[0]
# ratings.movieId = ratings.movieId.map(replace_name)

M = ratings.pivot_table(index=['userId'], columns=['movieId'], values='rating')
M = M.fillna(0)
# print (M.head(),"\n",M.shape)
# print(M.columns)

# print(M.columns)
#
# j = 1
# for i in M.columns:
#     while i != j:
#         print(i,"###########",j)
#         j += 1
#

l = np.ndarray(shape=3953)
ll = []
for i in M.columns:
    l[i] = 10

for i in range(0,3953):
    if l[i] != 10:
        ll.append(i)


print(len(ll))

pd.DataFrame(ll).to_csv("removed movies.csv")
exit()
M.to_csv("X_original_complete.csv")