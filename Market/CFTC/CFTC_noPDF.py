import blpapi
from xbbg import blp
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


List = [
    ['ES', 'Index', 'IMM0E', 'IMMTE'],
    ['NQ', 'Index', 'IMM3N', 'IMMPN'],
    ['DM', 'Index', 'CBT1D', 'CBTOD'],
    ['RTY', 'Index', 'CFF6T', 'CFC6T'],
    ['HWA', 'Index', 'CF30C', 'CC30C'],
    ['HWB', 'Index', 'CF30D', 'CC30D'],
    ['HWI', 'Index', 'CF30E', 'CC30E'],
    ['HWR', 'Index', 'CF30F', 'CC30F']
]

List = pd.DataFrame(List, columns=["Symbol", "YK", "Fut", "Fut&Option"])  # YK=YellowKey
S = List["Symbol"]
T = S + "A " + List["YK"]
BDP = blp.bdp(tickers=T.tolist(), flds=["name", "undl_spot_ticker", "exch_code", "contract_value"]).loc[T, :]

List[["Name", "Undl", "Exch", "Contract"]] = np.array(BDP)
List["MicroMini"] = "-"
List["Adj"] = "-"
for i in range(len(List)):
    tmp = List.loc[List["Undl"]==List.loc[i,"Undl"],"Symbol"].values[1]
    if tmp != List.loc[i,"Symbol"]:
        List.loc[i,"MicroMini"] = tmp
        List.loc[i,"Adj"] = 0.1


d_from = (pd.Timestamp.today()-pd.DateOffset(years=5)).strftime("%Y%m%d")
d_to = pd.Timestamp.today().strftime("%Y%m%d")

P = ["L","S","N"] 
tmp = List["Fut"]
T = [i + "NC" + j + " Index" for i in tmp for j in P]

for i in range(len(List)):
    tmp = List.loc[List["Undl"]==List.loc[i,"Undl"],"Symbol"].values[1]

BDH = blp.bdh(tickers=T, flds="px_last", start_date=d_from,end_date=d_to, Per="W", Days="W").reset_index()
BDH = BDH[["index"]+T]


T = [f"{List.loc[i, 'Symbol']}1 {List.loc[i, 'YK']}" for i in range(len(List))]
BDH2 = blp.bdh(tickers=T+["USDJPY Curncy"], flds="px_last", start_date=d_from,end_date=d_to, Days="W",Fill="P").reset_index()
BDH2 = BDH2[["index"]+T]

BDH2.columns = ["Date"] + [ i + "_last" for i in S]


df = BDH.copy()
df.columns = ['Date'] + [f'{i}_{j}' for i in List['Symbol'] for j in P]
df[df.columns[1:]] = df[df.columns[1:]].apply(lambda x: -x if x.name[-1] == 'S' else x)
df = df.merge(BDH2[['Date'] + [ i + "_last" for i in S]])
df.fillna(0, inplace=True)

def CFTC(s):
    fig, ax1 = plt.subplots(figsize=(10,4))
    Date = df["Date"]
    
    MM = List.loc[List["Symbol"]==s,"MicroMini"].values[0]
    
    if MM == "-":
        SL, SS, SN = [df[s+"_"+p] for p in P]
    else:
        Adj = List.loc[List["Symbol"]==s,"Adj"].values[0]
        SL, SS, SN = [df[s+"_"+p] + df[MM+"_"+p]*Adj for p in P]

    ax1.stackplot(Date, SL, labels=['Long'], color='lightsteelblue')
    ax1.stackplot(Date, SS, labels=['Short'], color="lightgrey")
    ax1.plot(Date, SN, label='Net', color="darkblue")
    ax2 = ax1.twinx()  
    ax2.plot(Date, df[s+"_last"], label='px_last(right)', color="red")  # Use the second y-axis for the fourth plot

    tmp = list(List.loc[List["Symbol"]==s,"Undl"])[0]
    plt.title("CFTC Speculative Positions for " + tmp)
    ax1.set_ylabel("Position(Amount)")
    
    ax1.legend(loc='upper left', bbox_to_anchor=(1.08, 1))
    ax2.legend(loc='upper right', bbox_to_anchor=(1.33, 0.7))
    fig.tight_layout()
    plt.show()
    
def CFTC_Net():
    fig, ax1 = plt.subplots(figsize=(10,4))
    Date = df["Date"]
    
    P = ['L', 'S', 'N']
    pos = {key: [0] * len(df) for key in P}

    for s in S[:4]:
        MM = List.loc[List["Symbol"]==s,"MicroMini"].values[0]
        Adj = List.loc[List["Symbol"]==s,"Adj"].values[0]
        for p in P:
            pos[p] += df[s+"_"+p] + df[MM+"_"+p]*Adj

    color_map = {'L': 'lightsteelblue', 'S': 'lightgrey', 'N': 'darkblue'}
    labels_map = {'L': 'Long', 'S': 'Short', 'N': 'Net'}

    for p in P:
        if p == 'N':
            ax1.plot(Date, pos[p], label=labels_map[p], color=color_map[p])
        else:
            ax1.stackplot(Date, pos[p], labels=[labels_map[p]], color=color_map[p])

    ax2 = ax1.twinx()
    ax2.plot(Date, df["ES_last"], label='px_last(right)', color="red")

    plt.title("CFTC Speculative Positions for Net (px_last:ES)")
    ax1.set_ylabel("Position(USD)")

    ax1.legend(loc='upper left', bbox_to_anchor=(1.08, 1))
    ax2.legend(loc='upper right', bbox_to_anchor=(1.33, 0.7))
    fig.tight_layout()
    plt.show()


for s in S[:4]:
    CFTC(s)
    
CFTC_Net()
