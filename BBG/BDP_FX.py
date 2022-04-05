from xbbg import blp

con = pdblp.BCon(timeout=10000)
con.start()

LS_EXJ = ["USD","EUR","GBP","CAD","AUD","NZD","CHF","NOK","SEK","HKD","CNH"]

T = []
T += [i  + "JPY BGN Curncy" for i in LS_EXJ]
# T += ["CSBS" + i + " TMUQ Curncy" for i in LS]  #Mitsubishi TTM

tmp = ["px_last","volatility_90d","rsi_30d"]
BDP = blp.bdp(tickers=T, flds=tmp)
BDP = BDP.loc[T,:]

for i in tmp:
    BDP.loc[:,i.lower()] = round(BDP.loc[:,i.lower()].astype(float),2)
BDP.insert(0, "Currency", LS_EXJ )
BDP.insert(1, "Ticker", T)
BDP.index = list(range(0, len(BDP)))
BDP
