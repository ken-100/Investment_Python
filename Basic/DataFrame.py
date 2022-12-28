import pandas as pd
import numpy as np

# pd.set_option('display.max_columns', 70)
# pd.set_option('display.max_rows', None)

df = pd.DataFrame(columns = ["A","B"])

df = pd.DataFrame(index = ["a","b"], columns = ["A","B"])
#      A    B
# a  NaN  NaN
# b  NaN  NaN

df = pd.DataFrame(np.zeros([2,2]), index = ["a","b"], columns = ["A","B"])
#      A    B
# a  0.0  0.0
# b  0.0  0.0

df = pd.DataFrame(np.zeros([2,2]))
c = pd.MultiIndex.from_arrays([["A", ""], ["x","y"]])
df.columns = c
#      A     
#      x    y
# 0  0.0  0.0
# 1  0.0  0.0



df1 = df
df2 = df.copy()
df.iloc[0,:] = 7

print(df1)
#      A     
#      x    y
# 0  7.0  7.0
# 1  0.0  0.0

print(df2)
#      A     
#      x    y
# 0  0.0  0.0
# 1  0.0  0.0




for i in range(0,3):
    exec(f"df{i} = df")

a =list(range(0,4))
print(a)
# [0, 1, 2, 3]

a = list(range(0,8,2))
print(a)
# [0, 2, 4, 6]

a = np.reshape(a,(2,2))
print(a)
# [[0 2]
#  [4 6]]

df = pd.DataFrame(a)
# print(df)
#    0  1
# 0  0  2
# 1  4  6

print(df.loc[df[0]==4,:])
#    0  1
# 1  4  6

#or
print(df.loc[(df[0]==0)|(df[0]==4),:])
#    0  1
# 0  0  2
# 1  4  6

(df[0]==0)|(df[0]==4)
# 0    True
# 1    True

#and
print(df.loc[(df[0]==0)&(df[1]==2),:])
#    0  1
# 0  0  2
# 1  4  6

print(df.loc[df[0].isin([0,4]),:])
#    0  1
# 0  0  2
# 1  4  6

print( df.loc[df[0].isin([0]),:] )
#    0  1
# 0  0  2

print( df.loc[~(df[0].isin([0])),:] ) #not in
#    0  1
# 1  4  6

print(df.loc[~(df[0].isin([0])),:].reset_index(drop=True))
#    index  0  1
# 0      1  4  6
