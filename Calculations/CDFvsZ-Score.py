from scipy import stats
from scipy.stats import norm
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

H = [x/2 for x in range(-6,7)]
tmp = pd.DataFrame( np.zeros([1,len(H)]),  index=["Z-Score"] )
tmp.loc["Z-Score",:] = H

for j in range(len(H)):
    tmp.loc["CDF",j] = round(stats.norm.cdf(H[j],0,1),2)

fig, ax = plt.subplots(1, 1, squeeze=False,figsize=(8,3),tight_layout=True)
ax[0,0].plot(tmp.iloc[0,:], tmp.iloc[1,:])
ax[0,0].set_title("Z-Score vs CDF")

print("Convert Z-Score to CDF")
plt.show()
tmp



H = [x/10 for x in range(1,10)]
tmp = pd.DataFrame( np.zeros([1,len(H)]),  index=["CDF"] )
tmp.loc["CDF",:] = H

for j in range(len(H)):
    tmp.loc["Z-Score",j] = round(norm.ppf(H[j]),2)
    
fig, ax = plt.subplots(1, 1, squeeze=False,figsize=(8,3),tight_layout=True)
ax[0,0].plot(tmp.iloc[0,:], tmp.iloc[1,:])
ax[0,0].set_title("CDF vs Z-Score")

print("Convert CDF to Z-Score")
plt.show()
tmp
