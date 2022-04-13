from xbbg import blp

con = pdblp.BCon(timeout=10000)
con.start()

LS_EXJ = ["USD","EUR","GBP","CAD","AUD","NZD","CHF","NOK","SEK","HKD","CNY"]

T = ["CSBS" + i + " TMUQ Curncy" for i in LS_EXJ]  #Mitsubishi TTM
# T = [i  + "JPY CMPN Curncy" for i in LS_EXJ] #CMPN

tmp = ["px_last","volatility_90d","rsi_30d"]
BDP = blp.bdp(tickers=T, flds=tmp)
BDP = BDP.loc[T,:]

for i in tmp:
    BDP.loc[:,i.lower()] = round(BDP.loc[:,i.lower()].astype(float),2)
BDP.insert(0, "Currency", LS_EXJ )
BDP.insert(1, "Ticker", T)
BDP.index = list(range(0, len(BDP)))
BDP

# https://data.bloomberglp.com/labs/sites/2/2013/12/blpapi-developers-guide-1.38.pdf
# https://data.bloomberglp.com/professional/sites/10/2017/03/BLPAPI-Core-Developer-Guide.pdf
