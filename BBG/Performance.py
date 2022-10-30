from xbbg import blp
import pdblp
import workdays
import datetime
import pandas as pd
import numpy as np
pd.set_option("display.max_columns", 70)


def ME(df):
    for i in range(1,len(df)):
        if df.loc[i,"Date"].month != df.loc[i-1,"Date"].month:
            if df.loc[i-1,"Date"].month ==3:
                df.loc[i-1,"ME"] = 3
            else:
                df.loc[i-1,"ME"] = 1

    df.loc[len(df)-1,"ME"] = 3
    
    return df
  
  
con = pdblp.BCon(timeout=5000)
con.start()

LS = ["ES","NQ","TP"]
T=[]
for i in range(0,len(LS)):
    T += [LS[i]+"1 Index"]
    
d_from = "20080301"
d_to = workdays.workday(datetime.datetime.today(), days=-1).strftime("%Y%m%d")

df = con.bdh(T, ["px_last"], d_from, d_to,
            elms = [("nonTradingDayFillOption","NON_TRADING_WEEKDAYS"),("nonTradingDayFillMethod","PREVIOUS_VALUE")]).reset_index()
df = df.loc[:,["date"]+T]
df.columns = ["Date"] + LS
df.insert(1,"ME",0)

df = ME(df)
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

tmp = Percent(Ret(3))
print("Yearly Ret",tmp.shape)
tmp


tmp = Percent(Ret(1))
print("Monthly Ret",tmp.shape)
tmp


def SD(k):
    tmp = df.loc[df["ME"]>=k,["Date"]+[x  for x in LS]]
    for j in LS:
        tmp.loc[:,j] =  tmp.loc[:,j].pct_change()

    tmp = tmp.iloc[1:].reset_index(drop=True)
    tmp = tmp.loc[:,LS]
    tmp = np.std(tmp) * 12**0.5

    SD = pd.DataFrame(np.zeros([len(tmp),2]),columns=["Name","SD"])
    SD["Name"] = LS
    SD["SD"] = tmp.values
    SD = SD.sort_values("SD", ascending=False).reset_index(drop=True)
    
    return SD
  
tmp = SD(3)
print("SD",tmp.shape)
tmp.loc[:,"SD"] = tmp.loc[:,"SD"].apply("{:.2%}".format)
tmp


def Corr(k):
    tmp = df.loc[df["ME"]>=k,["Date"]+[x  for x in LS]]

    for j in LS:
        tmp.loc[:,j] =  tmp.loc[:,j].pct_change()

    tmp = tmp.iloc[1:].reset_index(drop=True)
    tmp = tmp.loc[:,LS]

tmp = Corr(1)
print("Correlation")
tmp


def R(k,SD):
    tmp = Ret(3).iloc[[k],1:].T
    tmp1 =  ["Name","Ret","SD","Ratio"]

    YR = pd.DataFrame(np.zeros([len(tmp),len(tmp1)]),columns=tmp1)
    YR["Name"] = LS
    YR["Ret"] = tmp.values
    YR = YR.sort_values("Ret", ascending=False).reset_index(drop=True)

    for i in range(0,len(YR)):
        YR.loc[i,"SD"] = SD.loc[SD["Name"]==YR.loc[i,"Name"],"SD"].values

    YR.loc[:,"Ratio"] = YR.loc[:,"Ret"] / YR.loc[:,"SD"]

    for j in ["Ret","SD"]:
        YR.loc[:,j] = YR.loc[:,j].apply("{:.1%}".format)

    for j in ["Ratio"]:
        YR.loc[:,j] = YR.loc[:,j].apply("{:.2f}".format)

    return YR

SD_M = SD(3)
Ret_Y = Ret(3)
for i in range(0,len(Ret_Y)):    
    exec(f"YR{i}=R(i,SD_M)")
    

r = 3
c1 = []
for i in range(0,len(Ret_Y)):
    tmp = Ret_Y["Date"][i].strftime("%Y%m")
    c1 += [tmp]
    c1 += [" "]

Rank = pd.DataFrame( np.zeros([r,len(c1)]) )
c2 = ["Name","Ret"] * int(len(c1)/2)
c = pd.MultiIndex.from_arrays([c1, c2 ])
Rank.columns = c

Rank2 = pd.DataFrame( np.zeros([r,len(c1)]) )
c2 = ["Name","Ratio"] * int(len(c1)/2)
c = pd.MultiIndex.from_arrays([c1, c2 ])
Rank2.columns = c


for j in range(0,len(Ret_Y)):
    exec(f"tmp = YR{j}")
    Rank.iloc[:,0+2*j:2+2*j] = tmp.loc[0:r-1,['Name','Ret']].values
    
    tmp = tmp.sort_values("Ratio", ascending=False).reset_index(drop=True)
    Rank2.iloc[:,0+2*j:2+2*j] = tmp.loc[0:r-1,['Name','Ratio']].values

Rank
 
r = 3
c1 = []
for i in range(0,len(Ret_Y)):
    tmp = Ret_Y["Date"][i].strftime("%Y%m")
    c1 += [tmp]
    c1 += [" "]

Rank = pd.DataFrame( np.zeros([r,len(c1)]) )
c2 = ["Name","Ret"] * int(len(c1)/2)
c = pd.MultiIndex.from_arrays([c1, c2 ])
Rank.columns = c

Rank2 = pd.DataFrame( np.zeros([r,len(c1)]) )
c2 = ["Name","Ratio"] * int(len(c1)/2)
c = pd.MultiIndex.from_arrays([c1, c2 ])
Rank2.columns = c


i = 1
print(Ret_Y.loc[i,"Date"].strftime("%Y%m"))
exec(f"tmp=YR{i}")
tmp


for j in range(0,len(Ret_Y)):
    exec(f"tmp = YR{j}")
    Rank.iloc[:,0+2*j:2+2*j] = tmp.loc[0:r-1,['Name','Ret']].values
    
    tmp = tmp.sort_values("Ratio", ascending=False).reset_index(drop=True)
    Rank2.iloc[:,0+2*j:2+2*j] = tmp.loc[0:r-1,['Name','Ratio']].values
Rank
