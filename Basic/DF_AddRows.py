import numpy as np
import pandas as pd
import time
tmp = ["a" + str(x) for x in range(100)]


#Example
start = time.time()
df = pd.DataFrame(np.zeros([10000,10]))
df1 = pd.DataFrame(np.zeros([len(df),len(tmp)]), columns = tmp)
df = pd.concat([df ,df1],axis=1)
print(time.time() - start)


#Poor example1
start = time.time()
df = pd.DataFrame(np.zeros([10000,10]))
for j in tmp:
    df.loc[:,j] = 0
print(time.time() - start)

# <ipython-input-167-7e0798bdf66b>:4: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
#   df.loc[:,j] = 0

# C:\smtamsys\Anaconda3\lib\site-packages\pdblp\pdblp.py:278: FutureWarning: In a future version, `df.iloc[:, i] = newvals` will attempt to set the values inplace instead of always setting a new array. To retain the old behavior, use either `df[df.columns[i]] = newvals` or, if columns are non-unique, `df.isetitem(i, newvals)`
#   df.loc[:, 'date'] = pd.to_datetime(df.loc[:, 'date'])


#Poor example2
start = time.time()
df = pd.DataFrame(np.zeros([10000,10]))
for j in tmp:
    df[j] = 0
print(time.time() - start)
