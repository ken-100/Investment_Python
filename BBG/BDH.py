from xbbg import blp
import pdblp
import workdays
import datetime

con = pdblp.BCon(timeout=5000)
con.start()

LS = ["ES","NQ","TP"]
T=[]
for i in range(0,len(LS)):
    T += [LS[i]+"1 Index"]
    
# d_from = "20050301"
d_from = workdays.workday(datetime.datetime.today(), days=-260).strftime("%Y%m%d")
d_to = workdays.workday(datetime.datetime.today(), days=-1).strftime("%Y%m%d")

BDH = con.bdh(T, ["px_open","px_last"], d_from, d_to).reset_index()  
BDH.loc[:,["date"]+T].head()
