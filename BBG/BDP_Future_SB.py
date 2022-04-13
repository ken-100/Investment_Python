from xbbg import blp

LS = ["JB","TY","RX","TU","FV","US","WN","DU","OE","UB","OAT","IK","G ","CN","XM"]

T = [i + "A Comdty" for i in LS]
T1 = [i + "1 Comdty" for i in LS]

BDP = blp.bdp(tickers=T, flds=["name","currency","fut_ctd_isin"]).loc[T,:]


isin = BDP.loc[T,["fut_ctd_isin"]].dropna(how='all')
isin = [i for i in isin.loc[:,"fut_ctd_isin"]]

tmp0 = ["year","dur","yld"]
tmp1 = ["mty_years","dur_adj_bid","yld_ytm_bid"]
for i in tmp0:
    BDP.loc[:,i] = 0

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
BDP.index = list(range(0, len(BDP)))

print(BDP.shape)
BDP
