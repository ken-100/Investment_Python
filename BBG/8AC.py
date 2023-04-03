from xbbg import blp
import pdblp
import workdays
import datetime
from datetime import datetime, timedelta, date
con = pdblp.BCon(timeout=20000)
con.start()


def BDP(L):
    T = [i + " Index" for i in L]   
    BDP = blp.bdp(tickers=T, flds=["Security_name","long_comp_name","Currency","volatility_260d"]).loc[T,:]
    BDP.insert(0, "ticker", T)
    BDP = BDP.reset_index(drop=True)


    
    for i in range(len(BDP)):
        tmp = con.bdh(BDP.loc[i,"ticker"], ["px_last","tot_return_index_gross_dvds"], "20000101", "20230301")
        
        BDP.loc[i,"PR"] = round(tmp.iloc[len(tmp)-1,0] / tmp.iloc[0,0] - 1,2) 
        BDP.loc[i,"TR"] = round(tmp.iloc[len(tmp)-1,1] / tmp.iloc[0,1] - 1,2) 

        if tmp.iloc[len(tmp)-1,1] - tmp.iloc[len(tmp)-1,0] == 0:
            BDP.loc[i,"PR=TR"] = "1"
        else:
            BDP.loc[i,"PR=TR"] = ""

        BDP.loc[i,"Initial_TD"] = tmp.index[0].strftime("%Y%m%d")
    return BDP
    
    
    
print("Japan Stocks")
L = ["TPX","TPXDDVD"]
BDP(L)


print("Developed Country Stocks")
L = ["MBKO","M0KO","MXKO","M2KO","MAKO","MSHJKOK","GJ124280","HJ124336"]
BDP(L)


print("Emerging Markets Stocks")
L = ["GDUEEGF","NDUEEGF","HJ137561"]
BDP(L)


print("Developed Country REIT")
L = ["SREITWJJ","SREITJWJ"]
BDP(L)

print("Japan Bonds")
L = ["BPITTO01"]
BDP(L)

print("Developed Country Bond")
L = ["SBWGNJYC","SBWGNJYU"]
BDP(L)

print("Emerging Market Bond / USD Bond")
L = ["JPGCUJCP","JPGCHJCP","JPEIDIVR","JPGCCOMP"]
# L = ["JPGCUJCP","JPGCHJCP","JPEIDIVR","JPEIPLUS","JPEMCOMP","GBIE1545"]
tmp = BDP(L)
tmp


print("Emerging Market Bond / Local Currency Bond")
L = ["JGENDVUJ","JGENDVHJ","JGENGUJG","JGENGHJG","JGENVUJG","JGENVHJG"]
tmp = BDP(L)
tmp["Remarks"] = ["GBI EM Div"]*2+["GBI EM Global"]*2+["GBI EM Global Div"]*2
tmp
# https://www.jpmorgan.com/insights/research/index-research
# https://www.jpmorgan.com/content/dam/jpm/cib/complex/content/markets/index-research/Global-Index-Research-Product-Guide-2022.pdf#page=117
    
