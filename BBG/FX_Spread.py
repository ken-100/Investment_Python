import pdblp
from xbbg import blp
import datetime
import workdays
import pandas as pd
import numpy as np
from statistics import mean


con = pdblp.BCon(timeout=10000)
con.start()
term = "1M"

C = ["EUR","GBP","USD","CAD","AUD","NZD","CHF","NOK","SEK","CNH"]
T = [ x + "JPY" + term + " BGN Curncy" for x in C ]

d_from = "20210401"
d_to = workdays.workday(datetime.datetime.today(), days=-1).strftime("%Y%m%d")

F = ["px_ask","px_bid","px_last"]
bdh = con.bdh(T, F, d_from, d_to, elms = [("nonTradingDayFillOption","NON_TRADING_WEEKDAYS"),("nonTradingDayFillMethod","PREVIOUS_VALUE")]).reset_index()

S = pd.DataFrame(np.zeros([len(bdh),1]), columns = ["Date"]) #Spread
S.loc[:,"Date"] = bdh.loc[:,"date"]

tmp = ["ask","bid","last"]

for i in C:
    for j in tmp: 
        S.loc[:, i + "_" + j ] = bdh.loc[:,i + "JPY" + term + " BGN Curncy"]["px_" + j].values
        
    S.loc[:, i + "_Spread"] = S.loc[:, i + "_ask"] - S.loc[:, i + "_bid"]
    S.loc[:, i + "_Cost"] = S.loc[:, i + "_Spread"] / S.loc[:, i + "_last"]
S


F = ["Spread","Cost","last"]
SC = pd.DataFrame(np.zeros([len(C),len(F)]), index = C, columns = F)

for i in C:
    for j in F:
        SC.loc[i,j] = mean(S.loc[:, i + "_" + j])

tmp = ["Spread","last"]
for i in tmp: 
    SC.loc[:,i] = SC.loc[:,i].apply("{:.2f}".format)
SC.loc[:,"Cost"] = SC.loc[:,"Cost"].apply("{:.2%}".format)

print("vsJPY BothWays")
SC



# https://www.sbifxt.co.jp/service/detailedspread.html
SC_sbi = pd.DataFrame(np.zeros([len(C),len(F)]), index = C, columns = F)
SC_sbi.loc[:,"last"] = SC.loc[:,"last"].values

tmp = "Spread"

SC_sbi.loc["USD",tmp] = 0.4 / 100
SC_sbi.loc["EUR",tmp] = 0.5 / 100
SC_sbi.loc["GBP",tmp] = 0.9 / 100
SC_sbi.loc["AUD",tmp] = 0.6 / 100
SC_sbi.loc["NZD",tmp] = 1.2 / 100
SC_sbi.loc["CAD",tmp] = 2.5 / 100
SC_sbi.loc["CHF",tmp] = 2.8 / 100
SC_sbi.loc["SEK",tmp] = 2.8 / 100
SC_sbi.loc["NOK",tmp] = 3.5 / 100
SC_sbi.loc["CNH",tmp] = 2.5 / 100

for i in C:
    SC_sbi.loc[i,"Cost"] = SC_sbi.loc[i,"Spread"] / float(SC_sbi.loc[i,"last"])

SC_sbi.loc[:,"Cost"] = SC_sbi.loc[:,"Cost"].apply("{:.3%}".format)

print("vsJPY BothWays")
SC_sbi
