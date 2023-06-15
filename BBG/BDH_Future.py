from xbbg import blp
import pdblp
import workdays
import datetime
import pandas as pd
pd.set_option('display.max_columns', 70)

con = pdblp.BCon(timeout=5000)
con.start()

LS = ["ES","NQ","TP"]
T=[]
for i in range(len(LS)):
    T += [LS[i]+"1 Index"]
    
# d_from = "20050301"
d_from = workdays.workday(datetime.datetime.today(), days=-260).strftime("%Y%m%d")
d_to = workdays.workday(datetime.datetime.today(), days=-1).strftime("%Y%m%d")

BDH = con.bdh(T, ["px_open","px_last"], d_from, d_to).reset_index()
#BDH = con.bdh(T, ["px_open","px_last"], d_from, d_to, elms = [("periodicitySelection","MONTHLY")]  ).reset_index()  #Monthly
#BDH = con.bdh(T, ["px_open","px_last"], d_from, d_to, 
#        elms = [("nonTradingDayFillOption","NON_TRADING_WEEKDAYS"),("nonTradingDayFillMethod","PREVIOUS_VALUE")] ).reset_index()
#Formats the type of data returned for nontrading days.

BDH[["date"]+T].head()


# https://data.bloomberglp.com/labs/sites/2/2013/12/blpapi-developers-guide-1.38.pdf
# https://data.bloomberglp.com/professional/sites/10/2017/03/BLPAPI-Core-Developer-Guide.pdf
