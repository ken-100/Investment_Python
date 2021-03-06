from xbbg import blp
import pdblp

LS = ["TU","FV","TY","US","WN","DU","OE","RX","UB","OAT","IK","G ","CN","XM","JB"]

T = [i + "A Comdty" for i in LS]
T1 = [i + "1 Comdty" for i in LS]

BDP = blp.bdp(tickers=T, flds=["name","currency","fut_ctd_isin"]).loc[T,:]


isin = BDP.loc[T,["fut_ctd_isin"]].dropna(how='all')
isin = [i for i in isin.loc[:,"fut_ctd_isin"]]

tmp0 = ["year","dur","yld"]
tmp1 = ["mty_years","dur_adj_bid","yld_ytm_bid"]
# for i in tmp0:
#     BDP.loc[:,i] = 0

BDP1 = blp.bdp(tickers = [i+" Corp" for i in isin], flds=["mty_years","dur_adj_bid","yld_ytm_bid"])
for i in isin:
    for j in range(0,len(tmp0)):
        BDP.loc[BDP["fut_ctd_isin"]==i,tmp0[j]] = BDP1.loc[i+" Corp",tmp1[j]]

for i in tmp0:
    BDP.loc[:,i] = round(BDP.loc[:,i],2)

tmp0 = ["volume","vola"]
tmp1 = ["volume_avg_5d","volatility_90d"]
    

BDP1 = blp.bdp(tickers=T1, flds=tmp1).loc[T1,:]
for i in range(0,len(tmp0)):
    BDP.loc[:,tmp0[i]] = BDP1.loc[:,tmp1[i]].values

BDP.loc[:,"vola"] = round(BDP.loc[:,"vola"],2)

BDP.insert(0, "Ticker", LS)

for i in range(0,len(LS)):
    BDP.loc[BDP["Ticker"]==LS[i],"start_date"] = (con.bdh(T1[i], "px_last", "19991201", "20200101", elms = [("periodicitySelection","MONTHLY")]).reset_index().iloc[0,0]).strftime("%Y%m%d")
BDP = BDP.replace("19991231", "-")

BDP.index = list(range(0, len(BDP)))

print(BDP.shape)
BDP

# https://data.bloomberglp.com/labs/sites/2/2013/12/blpapi-developers-guide-1.38.pdf
# https://data.bloomberglp.com/professional/sites/10/2017/03/BLPAPI-Core-Developer-Guide.pdf
