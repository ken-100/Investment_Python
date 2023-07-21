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
import webbrowser


# path = r"C:\Users\ky090\OneDrive - The University of Texas at Austin\001_Market\100_Output"
path = r"S:\【1230】マルチ戦略運用U\30_業務用個人フォルダ\A1800401_山崎健\010_市場分析\000_News\000_Output" 
path = path.replace("\\", "/")
os.chdir(path)

ODA = workdays.workday(date.today(), days=-1) #One day agp
TDA= workdays.workday(date.today(), days=-2)  #Two days ago
OYA = TDA - relativedelta(months=13)
OYA = OYA.replace(day=calendar.monthrange(OYA.year, OYA.month)[1]) #One year ago
YE = date(TDA.year, 3, 31) if TDA.month > 3 or (TDA.month == 3 and TDA.day == 31) else date(TDA.year - 1, 3, 31)
ME = (date(TDA.year, TDA.month, 1) + relativedelta(months=-1, day=31)) #Month End


html = "<h3><u>Market Data as of " +ODA.strftime("%Y%m%d") + "</u></h3>"
def f(df,YK,field,html,flag=0,NC=0,diff=0):
    df = pd.DataFrame.from_dict(df, orient='index').reset_index(drop=False)
    df.columns = ["Ticker","Name"]

    if flag ==1:
        T = df.Ticker + "A Index"
        BDP = blp.bdp(tickers=T, flds=["country_iso","exch_code","crncy","undl_spot_ticker"]).loc[T,:]

        T = list(dict.fromkeys(BDP.undl_spot_ticker))
        T1 = pd.Series(T) + " Index"
        BDP1 = blp.bdp(tickers=T1, flds=["country_iso","crncy","security_name","name"]).loc[T1,:].reset_index()
        BDP1["index"] = T

        df["Crncy"] = BDP.crncy.tolist()
        df["Undl"] = BDP.undl_spot_ticker.tolist()
        df.insert(0, "Country", 0)
        df["Country"] = BDP1.set_index("index").loc[df["Undl"],"country_iso"].values
        
    if flag ==2:
        T = df.Ticker + "A Comdty"
        BDP = blp.bdp(tickers=T, flds=["fut_ctd_isin","mty_years","crncy"]).loc[T,:]
        df["Year"] = (BDP.mty_years.apply("{:,.1f}".format)).tolist()
        
        df.insert(0, "Country", 0)
        df["Country"] = [i[:2] for i in BDP.fut_ctd_isin]
    
    
    T = df.Ticker.tolist()
    T1 = (pd.Series(T) + YK).tolist()
    BDH = blp.bdh(T1, field, OYA, ODA, Calendar="5D", Fill="P").reset_index()
    BDH = BDH[["index"]+T1]    
    BDH.columns = ["Date"] + T
    
    if flag ==1:
        df = df.drop("Undl", axis=1)
        
    if flag >= 1:
        df["Country"] = df["Country"].where(df["Country"].shift() != df["Country"], "")
        
    if len(df) == len(df[df.Name==""]):
        df = df.drop("Name", axis=1)


    C = {"TDA":TDA,"ME":ME,"YE":YE}
    tmp = BDH.loc[len(BDH)-1, T]
    for i in C:
        if diff == 1:
            df[i] = (tmp - BDH.loc[BDH["Date"]==C[i].strftime("%Y%m%d"), T]).values[0]  
        else:
            df[i] = (tmp / BDH.loc[BDH["Date"]==C[i].strftime("%Y%m%d"), T] - 1).values[0]
        
    C = ["1D"] + [ME.strftime("%Y/%m/%d")[5:7].replace('0', '') + ME.strftime("%Y/%m/%d")[7:]] + [YE.strftime("%Y/%m/%d")[5:7].replace('0', '') + YE.strftime("%Y/%m/%d")[7:]]
    
    df.columns = df.columns[:df.shape[1]-3].tolist() + C

    if diff == 1:
        html += df.style\
            .bar(subset=C, align='mid', color=["pink", "lightblue"])\
            .format({c: '{:.2f}' for c in C})\
            .render()
    else:        
        html += df.style\
            .bar(subset=C, align='mid', color=["pink", "lightblue"])\
            .format({c: '{:.2%}' for c in C})\
            .render()

    if NC == 0:
        tmp = len(T) // 2 + len(T) % 2
        fig, ax = plt.subplots(tmp, 2,figsize=(10,tmp*2),tight_layout=True)
        for i in range(len(T)):
            ax[i//2,i%2].plot(BDH["Date"], BDH[T[i]])
            ax[i//2,i%2].set_title(T[i])

        plt.savefig("tmp.png")

        with open("tmp.png", "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        html += f'<img src="data:image/png;base64,{encoded_string}" width="850">'
        os.remove("tmp.png")

    html += "<h6>_________________________________________________________________________________________________________________________</h6>"
    

#     if diff == 1:
#         display(df.style\
#                 .bar(subset=C, align='mid', color=["pink", "lightblue"])\
#                 .format({c: '{:.2f}' for c in C})\
#                )
#     else:
#         display(df.style\
#                 .bar(subset=C, align='mid', color=["pink", "lightblue"])\
#                 .format({c: '{:.2%}' for c in C})\
#                )    

#     if NC == 0:
#         plt.show()
     
    return html


df = {
    'DM': ['Dow'],
    'ES': ['S&P500'],
    'NQ': ['Nasdaq'],
    'RTY': ['Russ2000(Small)'],
    'VG': ['EuroStox'],
    'GX': ['Dax'],
    'CF': ['CAC'],
    'Z ': ['FTSE100'],
    'SM': [''],
    'PT': [''],
    'XP': [''],
    'TP': ['Topix'],
    'TRE': ['Reit'],
    'HI': ['HangSeng'],
    'HC': ['Enterprises'],
    'XU': ['CHINA A50(SG)'],
    'IFB': ['CSI300(Large)'],
    'FFD': ['CSI500(Small)'],
    'JGS': ['Nifty50(SG)'],
    'NZ': ['Nifty50'],
    'AF': ['NiftyBank'],
    'TWT': ['FTSE_Taiwan(SG)'],
    'FT': ['TAIEX'],
    'KM': [''],
    'BZ': [''],
    'AI': ['']
}

html = f(df,"1 index","px_last",html,1)

df = {
    'S5CONS': ['Cons_Staple'],
    'S5ENRS': ['Energy'],
    'S5FINL': ['Financials'],
    'S5HLTH': ['Health_Care'],
    'S5INDU': ['Industrials'],
    'S5INFT': ['Information'],
    'S5MATR': ['Materials'],
    'S5TELS': ['COMM_SVC'],
    'S5UTIL': ['Utilities'],
    'S5COND': ['Cons_Discret'],
    'S5RLST': ['Real_Estate'],
    'RIY': ['Russell_1000'],
    'RTY': ['Russell_2000'],
    'RAY': ['Russell_3000'],
    'SPXL1': ['Eco'],
    'SOX': ['SOX'],
    'SPAC': ['SPAC'],
    'KRX': ['ReginalBank']
}

html = f(df," index","tot_return_index_gross_dvds",html)


df = {
    'CL': ['WTI(Oil)'],
    'CO': ['BRENT(Oil)'],
    'XB': ['Gasolin'],
    'NG': ['NaturalGas'],
    'KE': ['Coal(KEE)'],
    'TR': ['Coal(TRC)'],
    'GC': ['Gold'],
    'SI': ['Silver'],
    'PL': ['Platinum'],
    'HG': ['Cooper'],
    'IOE': ['Iron'],
    'LA': ['Alum'],
    'LN': ['Nickel'],
    'C ': ['Corn'],
    'S ': ['Soybean'],
    'W ': ['Wheat'],
    'LBO': ['Lumber']
}

html = f(df,"1 Comdty","px_last",html)


df = {
    'TU': [''],
    '3Y': [''],
    'FV': [''],
    'TY': [''],
    'UXY': [''],
    'US': [''],
    'TWE': [''],
    'WN': [''],
    'DU': [''],
    'OE': [''],
    'RX': [''],
    'UB': [''],
    'OAT': [''],
    'IK': [''],
    'WB': [''],
    'G ': [''],
    'JB': [''],
    'TFS': [''],
    'TFC': [''],
    'TFT': ['']
}

html = f(df,"1 Comdty","px_last",html,2,1)

df = {
    'GOVT US': [''],
    'AGG US': [''],
    'BND US': [''],
    'TIP US': [''],
    'SCHP US': ['']
}

html = f(df," Equity","tot_return_index_gross_dvds",html,0,1)


df = {
    'VIX': [''],
    'VIX9D': [''],
    'VIX1D': [''],
    'SKEW': [''],
    'MOVE': ['']
}

html = f(df," Index","px_last",html,0,0,1)

df = {
    'CESIUSD': [''],
    'CESIEUR': [''],
    'CESIJPY': ['']
}

html = f(df," Index","px_last",html,0,0,1)

df = {
    'IBOXUMAE': ['CDS_IG'],
    'IBOXHYSE': ['CDS_HY'],
    'ITRXEBE': ['CDS_Euro']
}

html = f(df," CBGN Index","px_last",html,0,0,1)



tmp = "EQ_" + datetime.today().strftime('%Y%m%d') + ".html"
with open(tmp, "w") as f:
    f.write(html)
webbrowser.open('file://' + os.path.realpath(tmp))