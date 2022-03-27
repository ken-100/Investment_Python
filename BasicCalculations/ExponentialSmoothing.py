from xbbg import blp
import pdblp
import workdays
import datetime
import pandas as pd
import numpy as np

con = pdblp.BCon(timeout=5000)
con.start()

T = ["ES1 Index","TY1 Comdty","JPY Curncy"]   #Ticker
LS = ["NQ","TY","JPY"]  #Symbol
    
# d_from = 19960628
d_from = workdays.workday(datetime.datetime.today(), days=-520).strftime("%Y%m%d")
d_to = workdays.workday(datetime.datetime.today(), days=-1).strftime("%Y%m%d")

df = con.bdh(T, ["px_last"], d_from, d_to).reset_index()
df.columns = ["Date"]+LS
for j in range(0,len(LS)):    
    df.loc[:,LS[j]+"_RetD"]=df.loc[:,LS[j]].pct_change()

p = 260   #Period
h = 10    #Half Life
v = 0.5 ** (np.arange(p,0,-1)/h)
v = v/sum(v)

for j in range(0,len(LS)):
    df.loc[:, LS[j] + "_HR"] = 0
    for i in range(p,len(df)):
        HR = 1
        for k in range(0,p):
            HR *=  (1+df.loc[i-p+k+1,LS[j]+"_RetD"])**v[k]
            df.loc[i, LS[j]+"_HR"] = HR**260 -1

for j in range(0,len(LS)):
    df.loc[:, LS[j]+"_SD"] = 0
    for i in range(p,len(df)):
        tmp = np.dot(df.loc[i-p+1:i,LS[j]+"_RetD"]**2,v) - np.dot(df.loc[i-p+1:i,LS[j]+"_RetD"],v)**2
        df.loc[i, LS[j]+"_SD"] = ( tmp * 260 )**0.5

for j in range(0,len(LS)):
    for k in range(j+1,len(LS)):
        df.loc[:, LS[j]+"-"+LS[k]+"_Cov"] = 0
        df.loc[:, LS[j]+"-"+LS[k]+"_Cor"] = 0
        for i in range(p,len(df)):
            tmp = np.dot(df.loc[i-p+1:i,LS[j]+"_RetD"]*df.loc[i-p+1:i,LS[k]+"_RetD"],v)
            tmp -= np.dot(df.loc[i-p+1:i,LS[j]+"_RetD"],v) * np.dot(df.loc[i-p+1:i,LS[k]+"_RetD"],v)
            df.loc[i, LS[j]+"-"+LS[k]+"_Cov"] = tmp * 260
            df.loc[i, LS[j]+"-"+LS[k]+"_Cor"] = tmp * 260 / df.loc[i, LS[j]+"_SD"] / df.loc[i, LS[k]+"_SD"]

df
