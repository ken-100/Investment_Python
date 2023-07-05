import pdblp
from xbbg import blp
import workdays
import time
import datetime
import pandas as pd
import numpy as np
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
import calendar

pd.set_option('display.max_columns', 70)
# https://smart-hint.com/python/style/
# https://www.salesanalytics.co.jp/datascience/datascience046/

ODA = workdays.workday(date.today(), days=-1).strftime("%Y%m%d") #One day agp
TDA= workdays.workday(date.today(), days=-2)  #Two days ago

if TDA.month > 3 or (TDA.month == 3 and TDA.day == 31):
    YE = date(TDA.year, 3, 31).strftime("%Y%m%d")
else:
    YE = date(TDA.year - 1, 3, 31).strftime("%Y%m%d")
    
L = ["NZD","NOK","AUD","CNY","EUR","CAD","GBP","CHF","JPY","SEK"]
T = [i + "USD BGN Curncy" for i in L] 
df = blp.bdh(T, "px_last", YE, ODA, Days="W", Fill="P").reset_index()
df = df[["index"]+T]
df.columns = ["Date"] + L


T0 = [i + " BGN Curncy" for i in L]
T1 = [i + "1M BGN Curncy" for i in L]
T1 = [x.replace("CNY", "CNH") for x in T1]

BDP0 = blp.bdp(tickers=T0, flds=["px_last","fwd_scale","is_pct_chg_app_base_crncy"]).loc[T0,:]
BDP1 = blp.bdp(tickers=T1, flds=["px_last"]).loc[T1,:]

BDP = BDP0.reset_index(drop=True)
BDP.insert(0, "Curncy", L)
BDP.insert(2, "frd_point", BDP1["px_last"].tolist())
BDP.insert(3, "Carry", 0)

BDP["Carry"] = (1 + BDP["frd_point"] / BDP["px_last"] / 10 ** BDP["fwd_scale"] ) ** 12 - 1


TDA= workdays.workday(date.today(), days=-2) #Two days ago
ME = (date(TDA.year, TDA.month, 1) + relativedelta(months=-1, day=31)).strftime("%Y/%m/%d") #Month End
YE = date(TDA.year, 3, 31) if TDA.month > 3 or (TDA.month == 3 and TDA.day == 31) else date(TDA.year - 1, 3, 31) #Year End
YE = YE.strftime("%Y/%m/%d")
TDA = TDA.strftime("%Y/%m/%d")  

C = ["TDA","ME","YE"]
FX = pd.DataFrame(L, columns=["Curncy"])

tmp = df.loc[len(df)-1, L]

for i in C:
    exec(f"d = {i}")
    FX[i] = (tmp / df.loc[df["Date"]==d, L] - 1).values[0]

FX.sort_values(by=C[0], ascending=False, inplace=True)
FX["Carry"] = np.where(BDP["is_pct_chg_app_base_crncy"] == "Y", BDP["Carry"], -BDP["Carry"])

C = ["Currency","1D","vs"+ME[5:],"vs"+YE[5:],"Carry"]
FX.columns= C

print("Currency Return as of "+ODA+" (vsUSD)")
display(FX.style\
        .bar(subset=[C[1]],align='mid',color=["pink","lightblue"])\
        .bar(subset=[C[2]],align='mid',color=["pink","lightblue"])\
        .bar(subset=[C[3]],align='mid',color=["pink","lightblue"])\
        .bar(subset=[C[4]],align='mid',color=["pink","lightblue"])\
        .format({C[1]: '{:.2%}'})\
        .format({C[2]: '{:.2%}'})\
        .format({C[3]: '{:.2%}'})\
        .format({C[4]: '{:.2%}'})\
       )
