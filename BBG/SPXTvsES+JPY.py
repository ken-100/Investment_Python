from xbbg import blp
import pdblp
import workdays
import datetime
import pandas as pd
import matplotlib.pyplot as plt
pd.set_option('display.max_columns', 70)

con = pdblp.BCon(timeout=5000)
con.start()


T = ["SPXT Index","ES1 Index","SBUS13L Index","SBUS13YC Index","JPY BGN Curncy"]
    
d_from = "20070301"
# d_from = workdays.workday(datetime.datetime.today(), days=-260).strftime("%Y%m%d")
d_to = workdays.workday(datetime.datetime.today(), days=-1).strftime("%Y%m%d")

BDH = con.bdh(T, "px_last", d_from, d_to, 
       elms = [("nonTradingDayFillOption","NON_TRADING_WEEKDAYS"),("nonTradingDayFillMethod","PREVIOUS_VALUE")] ).reset_index()

BDH = BDH.loc[:,["date"]+T]
BDH.head()


df = pd.DataFrame(BDH["date"].values,columns = ["Date"])
def ME(df):
    df.loc[:,"ME"] = 0
    for i in range(1,len(df)):
        if df.loc[i,"Date"].month != df.loc[i-1,"Date"].month:
            if df.loc[i-1,"Date"].month ==3:
                df.loc[i-1,"ME"] = 3
            else:
                df.loc[i-1,"ME"] = 1
    df.loc[len(df)-1,"ME"] = 3    
    return df

df = ME(df)


df["SPXT"] = BDH["SPXT Index"].pct_change()
df["JPY"] = BDH["JPY BGN Curncy"].pct_change()
df["SPXT_JPY"] = (BDH["SPXT Index"] * BDH["JPY BGN Curncy"]).pct_change()

df["ES"] = BDH["ES1 Index"].pct_change()
df["HC"] = BDH["SBUS13YC Index"].pct_change() - BDH["SBUS13L Index"].pct_change()

df["ES+JPY"] = df["ES"] - df["HC"] + df["JPY"] 




df["SPXT_JPY_Index"] = 100
df.loc[1:,"SPXT_JPY_Index"] = ( 1 + df.loc[1:,"SPXT_JPY"] ).cumprod()*100

df["ES+JPY_Index"] = 100
df.loc[1:,"ES+JPY_Index"] = ( 1 + df.loc[1:,"ES+JPY"] ).cumprod()*100

df["HC_Index"] = 100
df.loc[1:,"HC_Index"] = ( 1 + df.loc[1:,"HC"] ).cumprod()*100

df


def Ret(k):
    tmp = df.loc[df["ME"]>=k,["Date"]+[x  for x in LS]]

    for j in LS:
        tmp.loc[:,j] =  tmp.loc[:,j].pct_change()
    tmp = tmp.iloc[1:].reset_index(drop=True)
    tmp = tmp.loc[:,["Date"]+LS]
    return tmp

def Percent(tmp):
    for i in range(0,len(tmp)):
        tmp.iloc[i,1:] = tmp.iloc[i,1:].apply("{:.1%}".format)
    return tmp

LS = ["SPXT_JPY_Index","ES+JPY_Index"]
tmp = Ret(3)
tmp["Diff"] = tmp[LS[0]] - tmp[LS[1]]
tmp  = Percent(tmp)
tmp


import matplotlib.pyplot as plt
fig, ax = plt.subplots(1, 2, squeeze=False,figsize=(8,3),tight_layout=True)

x = df.loc[:,"Date"]

ax[0,0].plot(x, df.loc[:,"SPXT_JPY_Index"])
ax[0,0].plot(x, df.loc[:,"ES+JPY_Index"])
ax[0,1].set_title("Shadow")
ax[0,1].plot(x, df.loc[:,"HC_Index"])
plt.show()
