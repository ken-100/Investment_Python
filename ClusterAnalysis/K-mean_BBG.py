from xbbg import blp
import pdblp
import workdays
import datetime
from sklearn.cluster import KMeans
import pandas as pd

LS = ["ES","NQ","RTY","VG","GX","Z ","PT","XP","TP","HI","XU","IH"]

T=[]
T1=[]
for i in range(0,len(LS)):
    T += [LS[i]+"A Index"]
    T1 += [LS[i]+"1 Index"]
    
BDP = blp.bdp(tickers=T, flds=["name","currency","undl_spot_ticker"])
BDP = BDP.loc[T,:]

BDP1 = blp.bdp(tickers=T1, flds=["volume_avg_5d","volatility_90d"])
BDP1 = BDP1.loc[T1,:]

undl = BDP.loc[T,["undl_spot_ticker"]].loc[T,:] + " Index"

tmp=[]
for i in range(0,len(undl)):
    tmp += [undl.iloc[i,0]]
tmp = blp.bdp(tickers=tmp, flds="country_iso").loc[tmp,"country_iso"]
BDP.loc[:,"country"] = BDP.loc[:,"name"]
for i in range(0,len(T)):
    BDP.loc[:,"country"][i] = tmp[i]
    
    undl = BDP.loc[T,["undl_spot_ticker"]].loc[T,:] + " Index"
tmp=[]
for i in range(0,len(undl)):
    tmp += [undl.iloc[i,0]]
tmp = blp.bdp(tickers=tmp, flds="country_iso").loc[tmp,"country_iso"]

for i in range(0,len(T)):
    BDP.loc[:,"country"][i] = tmp[i]
BDP.loc[:,"volume"] = BDP1.loc[:,"volume_avg_5d"].values
BDP.loc[:,"vola"] = BDP1.loc[:,"volatility_90d"].values
BDP.loc[:,"vola"] = round(BDP.loc[:,"vola"],1)
# BDP.index = LS
BDP.insert(0, "Ticker", LS)
BDP.index = list(range(0, len(BDP)))

#Get Historidcal Data
con = pdblp.BCon(timeout=5000)
con.start()

d_from = workdays.workday(datetime.datetime.today(), days=-260).strftime("%Y%m%d")
d_to = workdays.workday(datetime.datetime.today(), days=-1).strftime("%Y%m%d")

df = con.bdh(T1, ["px_last"], d_from, d_to).reset_index()
#df = con.bdh(T1, ["px_last"], d_from, d_to,elms = [("periodicitySelection","WEEKLY")]).reset_index() #Weekly
df = df.loc[:,["date"]+T1]
df.columns = ["Date"]+LS

for j in range(0,len(LS)):    
    df.loc[:,LS[j]+"_RetD"]=df.loc[:,LS[j]].pct_change()

#K-means
tmp = [x + "_RetD" for x in LS]
df_Ret = df.loc[1:,tmp].reset_index(drop=True)

c = KMeans(n_clusters=4,random_state=3).fit_predict(df_Ret.T) #pred_cluster
# c = KMeans(n_clusters=4,init='k-means++',random_state=3).fit_predict(df_Ret.T)

df2 = pd.DataFrame(BDP.values)
df2.columns = BDP.columns

df2.insert(0,"Group",c)
df2 = df2.sort_values(by='Group').reset_index(drop=True)
df2
