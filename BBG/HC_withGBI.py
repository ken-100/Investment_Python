import pdblp
from xbbg import blp
import pandas as pd
import workdays
import datetime
import numpy as np

con = pdblp.BCon(timeout=10000)
con.start()

C = ["US","DM","UK","CD","AD","NZ","SZ","NK","SK"]

T0 = ["L","YC"]
tmp = ["Currency","country_iso","px_last","volatility_90d","rsi_30d"]

for i in T0:
    T = ["SB" + x + "13" + i + " Index" for x in C]
    BDP0 = blp.bdp(tickers=T, flds=tmp)
    BDP0 = BDP0.loc[T,:]

    for j in tmp[2:]:
        BDP0.loc[:,j.lower()] = round(BDP0.loc[:,j.lower()].astype(float),2)
    
    BDP0.insert(1, "Ticker", T)
    BDP0.index = list(range(0, len(BDP0)))
    
    exec(f"T{i} = T")
    exec(f"BDP{i} = pd.DataFrame(BDP0.values, columns = BDP0.columns)")

    
BDPYC.loc[:,"currency"] = BDPL.loc[:,"currency"] 
BDPYC.loc[:,"country_iso"] = BDPL.loc[:,"country_iso"] 

BDPL
BDPYC

d_from = "20040901"
d_to = workdays.workday(datetime.datetime.today(), days=-1).strftime("%Y%m%d")
Currency = list(BDPYC['currency'])

for i in T0:
    
    exec(f"T = T{i}")
    tmp = con.bdh(T, "px_last", d_from, d_to,
                 elms = [("nonTradingDayFillOption","NON_TRADING_WEEKDAYS"),("nonTradingDayFillMethod","PREVIOUS_VALUE")]).reset_index()

    GBI = pd.DataFrame(np.zeros([len(tmp),len(T)+1]), columns = ["Date"]+T)
    GBI.loc[:,"Date"] = tmp.loc[:,"date"]

    for j in T:
        GBI.loc[:,j] = tmp.loc[:,j].values
        
    exec(f"GBI{i} = pd.DataFrame(GBI.values, columns = ['Date'] + Currency)")

GBIL


    
HC = pd.DataFrame(np.zeros([len(GBIL),GBIL.shape[1]+1]),columns=["Date","ME"]+list(GBIL.columns[1:]))

HC["Date"] = GBIL["Date"]
for i in range(1,len(HC)):
    if HC.loc[i,"Date"].month != HC.loc[i-1,"Date"].month:
        if HC.loc[i-1,"Date"].month ==3:
            HC.loc[i-1,"ME"] = 3
        else:
            HC.loc[i-1,"ME"] = 1
HC.loc[len(HC)-1,"ME"] = 3

for i in Currency:
    HC.loc[1:,i] = GBIYC[i].pct_change() - GBIL[i].pct_change() 
  
for i in Currency:
    HC.loc[:,i+"_Index"] = 100
    HC.loc[1:,i+"_Index"] = (1+HC.loc[1:,i]).cumprod()*100
    
HCM = HC.loc[HC["ME"]>=3,["Date"]+[x + "_Index" for x in Currency]]

for i in Currency:
    HCM.loc[1:,i] = HCM.loc[1:,i+"_Index"].pct_change()

HCM = HCM.iloc[1:].reset_index(drop=True)
HCM = HCM.loc[:,["Date"]+Currency]
for i in range(0,len(HCM)):
    HCM.iloc[i,1:] = HCM.iloc[i,1:].apply("{:.1%}".format)
HCM
