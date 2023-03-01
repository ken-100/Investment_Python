import pandas as pd
import numpy as np
import time


NP= np.random.rand(int(1e5),2)
PD = pd.DataFrame(NP)
NP = PD.values



start = time.time()
for i in range(len(NP)):
    NP[i,0] = 0
    NP[i,1] = 1

print(round(time.time() - start,2),"Seconds")
pd.DataFrame(NP).head()
# 0.03 Seconds



start = time.time()
for i in range(len(PD)):
    PD.loc[i,0] = 0
    PD.loc[i,1] = 1

print(round(time.time() - start,2),"Seconds")
PD.head()
# 11.82 Seconds
