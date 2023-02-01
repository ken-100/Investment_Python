import pandas as pd
import numpy as np

df = pd.DataFrame(np.zeros([2,2]), index = ["a","b"], columns = ["A","B"])
df
#   A   B
# a 0.0 0.0
# b 0.0 0.0


df.rename({"a":"z"})
#   A   B
# z 0.0 0.0
# b 0.0 0.0

df.rename({"A":"Z"},axis=1)
#   Z   B
# a 0.0 0.0
# b 0.0 0.0


tmp = np.array([[0,1], [2,3]])
df = pd.DataFrame(tmp)

tmp = np.array(range(4)).reshape(2, 2)
df = pd.DataFrame(tmp)
df
#   0 1
# 0 0 1
# 1 2 3


df = df.sort_values(by=1,axis=1,ascending=False)
df
#   1 0
# 0 1 0
# 1 3 2

df.sort_values(by=1,axis=1)
#   0 1
# 0 0 1
# 1 2 3


df = pd.DataFrame( index = ["a","b"], columns = ["A","B"])
df
#   A   B
# a NaN NaN

df.fillna(1)
#   A B
# a 1 1
# b 1 1

df.fillna({'A': 1, 'B': 2})
#   A B
# a 1 2
# b 1 2

df.fillna({'A': 1})
#   A B
# a 1 NaN
# b 1 NaN
# b NaN NaN

df = pd.DataFrame( index = ["a","b"], columns = ["A","B"])
df.loc["a",:] = 1
df

#   A   B
# a 1   1
# b NaN NaN


df.dropna(how='all')
#   A B
# a 1 1

df = pd.DataFrame( index = ["a","b"], columns = ["A","B"])

df.loc[:,"A"] = 1
df = df.assign(A=1)  #Same meaning

df
#   A B
# a 1 NaN
# b 1 NaN

df.dropna(how='all', axis=1)
#   A
# a 1
# b 1



df0 = pd.DataFrame(np.zeros([2,2]), index = ["a","b"], columns = ["A","B"])
df1 = pd.DataFrame(np.ones([2,2]), index = ["c","d"], columns = ["A","B"])
# df0.append(df1) #should be avoided
df = pd.concat([df0,df1])
df
#   A   B
# a 0.0 0.0
# b 0.0 0.0
# c 1.0 1.0
# d 1.0 1.0


df0 = pd.DataFrame(np.zeros([2,2]), index = ["a","b"], columns = ["A","B"])
df1 = pd.DataFrame(np.ones([2,2]), index = ["c","d"], columns = ["A","D"])
# df0.append(df1) #should be avoided
df = pd.concat([df0,df1])
df
#   A   B   D
# a 0.0 0.0 NaN
# b 0.0 0.0 NaN
# c 1.0 NaN 1.0
# d 1.0 NaN 1.0


pd.DataFrame(df).to_csv('df.csv')
