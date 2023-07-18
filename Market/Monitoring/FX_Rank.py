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
import base64
import matplotlib.pyplot as plt
import os
import argparse

# parser = argparse.ArgumentParser()
# parser.add_argument('path')
# args = parser.parse_args()

ODA = workdays.workday(date.today(), days=-1).strftime("%Y%m%d") #One day agp
TDA= workdays.workday(date.today(), days=-2)  #Two days ago
OYA = TDA - relativedelta(months=13)
OYA = OYA.replace(day=calendar.monthrange(OYA.year, OYA.month)[1]) #One year ago

if TDA.month > 3 or (TDA.month == 3 and TDA.day == 31):
    YE = date(TDA.year, 3, 31).strftime("%Y%m%d")
else:
    YE = date(TDA.year - 1, 3, 31).strftime("%Y%m%d")
    
L = ["JPY","EUR","CNY","GBP","CAD","AUD","NZD","CHF","NOK","SEK"]
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

L2 = [row['Curncy'] + 'USD' if row['is_pct_chg_app_base_crncy'] == 'N' else 'USD' + row['Curncy'] for _, row in BDP.iterrows()]
L2 += [i + "JPY" for i in L[1:]] + ["CHFNOK"]
T2 = [i + " BGN Curncy" for i in L2]
df2 = blp.bdh(T2, "px_last", OYA, ODA, Days="W", Fill="P").reset_index()
df2 = df2[["index"]+T2]
df2.columns = ["Date"] + L2

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


FX["Carry"] = np.where(BDP["is_pct_chg_app_base_crncy"] == "Y", BDP["Carry"], -BDP["Carry"])
FX.sort_values(by="TDA", ascending=False, inplace=True)
FX = FX.reset_index(drop=True)

C = ["Currency","1D","vs"+ME[5:],"vs"+YE[5:],"Carry"]
FX.columns= C


html = FX.style\
    .bar(subset=C[1:], align='mid', color=["pink", "lightblue"])\
    .format({c: '{:.1%}' for c in C[1:]})\
    .render()

tmp = len(L2) // 2 + len(L2) % 2
fig, ax = plt.subplots(tmp, 2,figsize=(10,tmp*2),tight_layout=True)
for i in range(len(L2)):
    ax[i//2,i%2].plot(df2["Date"], df2[L2[i]])
    ax[i//2,i%2].set_title(L2[i])
plt.savefig("tmp.png")

with open("tmp.png", "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read()).decode()
html += f'<img src="data:image/png;base64,{encoded_string}">'

html = "<h3><u>as of " +ODA + "</u></h3>" + html


# path = args.path
path = r"C:\Users\ky090\OneDrive - The University of Texas at Austin\001_Market\100_Output"

path = path.replace("\\", "/")
os.chdir(path)
print(os.getcwd())
with open("FX_" + datetime.now().strftime('%Y%m%d') + ".html", "w") as f:
    f.write(html)
    

print("Currency Return as of "+ODA+" (BGN, vsUSD)")
display(FX.style\
        .bar(subset=C[1:], align='mid', color=["pink", "lightblue"])\
        .format({c: '{:.1%}' for c in C[1:]})\
       )

plt.show()
