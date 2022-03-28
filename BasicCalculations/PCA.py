import pdblp
from xbbg import blp
import workdays
import datetime
import numpy as np
import pandas as pd

T = ["BPITTO01 Index","SBWGNJYC Index","SBUSJYC Index","TPXDDVD Index","TPXDREIT Index","M0KO Index","SREITJWJ Index"]
T += ["USDJPYCR CMPN Curncy","EURJPYCR CMPN Curncy"]
LS = ["SBJ","SBF","SBU","EQJ","REJ","EQF","REF","USD","EUR"]


con = pdblp.BCon(timeout=5000)
con.start()

d_from = workdays.workday(datetime.datetime.today(), days=-260).strftime("%Y%m%d")
d_to = workdays.workday(datetime.datetime.today(), days=-1).strftime("%Y%m%d")
df = con.bdh(T, ["px_last"], d_from, d_to,elms = [("nonTradingDayFillMethod","PREVIOUS_VALUE"),("nonTradingDayFillOption","NON_TRADING_WEEKDAYS")]).reset_index()   #blp.bdhでもok

df = df.loc[:,["date"]+T]
df.columns = ["Date"] + LS
df.insert(loc = 1, column= "ME", value= 0) #MonthEnd

for i in range(2,len(df)):
    if df.loc[i,"Date"].month != df.loc[i-1,"Date"].month:
        if df.loc[i-1,"Date"].month ==3:
            df.loc[i-1,"ME"] = 5 #Year
        elif df.loc[i-1,"Date"].month ==9:
            df.loc[i-1,"ME"] = 3 #Halfyear
        elif df.loc[i-1,"Date"].month in [6,12]:
            df.loc[i-1,"ME"] = 2 #Quater
        else:
            df.loc[i-1,"ME"] = 1
df.loc[len(df)-1,"ME"] = 5

df = df.loc[df["ME"]>=1,:].reset_index(drop=True)

for i in LS:
    df.loc[:,i] = df.loc[:,i].pct_change()

df = df.iloc[1:,:].reset_index(drop=True)


Cor = df[LS].corr()

val, vec = np.linalg.eig(Cor)


vec = pd.DataFrame(vec)
for i in range(0,len(vec)):
    vec.iloc[i,:] = vec.iloc[i,:].apply("{:.2f}".format)


val /=  sum(val)
val = pd.DataFrame(val)
print(val)


vec.index = LS
for i in range(0,len(Cor)):
    Cor.iloc[i,:] = Cor.iloc[i,:].apply("{:.2f}".format)
vec
