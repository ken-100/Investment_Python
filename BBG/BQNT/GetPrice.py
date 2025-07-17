import bql
import pandas as pd
import numpy as np

def create_df(ticker):
    
    bq = bql.Service()
    u = bq.univ
    d = bq.data
    f = bq.func

    ticker += ' Equity'
    dt = f.range('-1m', '-1d')


    data = {
        'price': d.px_last(dates=dt).dropna(),
    }
    req = bql.Request(ticker, data, preferences=dict(dropcols=['currency']))
    res = bq.execute(req)
    df = bql.combined_df(res)
    df = df.reset_index(drop=True)
    df.columns = ["Date","Price"]

    return df



List = ["AAPL US","GOOGL US","MSFT US"]


df_list = {}
for i, l in  enumerate(List):
     df_list[i] = create_df(l)
    

                  
price_cols = [df_list[i]["Price"] for i in range(len(List))]
df = pd.concat([df_list[0]["Date"]] + price_cols, axis=1)
df.columns = ["Date"] + List
df


bq = bql.Service()



# universe = ['AAPL US Equity','CRWD US Equity','SNAP US Equity']
# data_item = bq.data.price(dates=bq.func.range('-2D', '0D'), fill='PREV', pricing_source='BGN')

# request = bql.Request(universe, data_item)
# response = bq.execute(request)

# data = response[0].df()
# data

