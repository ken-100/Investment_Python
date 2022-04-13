import pdblp
from xbbg import blp
import workdays
import time
import datetime
import pandas as pd
pd.set_option('display.max_columns', 70)

##### BDP
con = pdblp.BCon(timeout=10000)
con.start()

LS_EXJ = ["USD","EUR"]
# LS_EXJ = ["USD","EUR","GBP","CAD","AUD","NZD","CHF","NOK","SEK","HKD","CNY"]

T = ["CSBS" + i + " TMUQ Curncy" for i in LS_EXJ]  #Mitsubishi TTM
# T = [i  + "JPY CMPN Curncy" for i in LS_EXJ] #CMPN

tmp = ["px_last","volatility_90d","rsi_30d"]
BDP = blp.bdp(tickers=T, flds=tmp)
BDP = BDP.loc[T,:]
BDP

##### TTM
for i in tmp:
    BDP.loc[:,i.lower()] = round(BDP.loc[:,i.lower()].astype(float),2)
BDP.insert(0, "Currency", LS_EXJ )
BDP.insert(1, "Ticker", T)
BDP.index = list(range(0, len(BDP)))


con = pdblp.BCon(timeout=10000)
con.start()

d_from = "20050301"
d_to = "20211027"
d_to = workdays.workday(datetime.datetime.today(), days=-1).strftime("%Y%m%d")

TTM = con.bdh(T, "px_open", d_from, d_to,
             elms = [("nonTradingDayFillOption","NON_TRADING_WEEKDAYS"),("nonTradingDayFillMethod","PREVIOUS_VALUE")]).reset_index()
TTM = TTM.loc[:,["date"]+T]
TTM.head()

##### CMPN
LSP = []
T2 = []
LS = LS_EXJ + ["JPY"]
for i in range(0,len(LS)):
    for j in range(i+1,len(LS)):
        tmp = LS[i] + LS[j]
        LSP += [ tmp ]
        T2 += [ tmp + " CMPN Curncy" ]

CMPN = con.bdh(T2, "px_last", d_from, d_to,
             elms = [("nonTradingDayFillOption","NON_TRADING_WEEKDAYS"),("nonTradingDayFillMethod","PREVIOUS_VALUE")]).reset_index()
CMPN = CMPN.loc[:,["date"]+T2]
CMPN.head()

# https://data.bloomberglp.com/labs/sites/2/2013/12/blpapi-developers-guide-1.38.pdf
# https://data.bloomberglp.com/professional/sites/10/2017/03/BLPAPI-Core-Developer-Guide.pdf
