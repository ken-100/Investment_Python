import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


p = 260
H = [10,20,40,60,120,260]
H = [5,10,15,20,25] + list(range(30,280,10))

tmp = pd.DataFrame(index=["HalfPeriod","Ave"])
tmp = pd.DataFrame( np.zeros([1,len(H)]),  index=["HalfPeriod"] )
tmp.loc["HalfPeriod",:] = H

for j,h in enumerate(H):
    v = 0.5 ** (np.arange(p,0,-1)/h)
    v /= sum(v)    
    tmp.loc["Ave",j] = round(np.dot(v,list(range(p,0,-1))),1)

tmp.loc["Diff",:] = 0 
for j in range(1,len(H)):
    tmp.loc["Diff",j] = tmp.loc["Ave",j]  - tmp.loc["Ave",j-1] 

fig, ax = plt.subplots(1, 1, squeeze=False,figsize=(8,3),tight_layout=True)
ax[0,0].plot(tmp.iloc[0,:], tmp.iloc[1,:])
ax[0,0].set_title("HalfPeriod vs AveDays")

print("TCA Trend: EQ=83, SB=120, FX=11or85")
plt.show()
tmp
