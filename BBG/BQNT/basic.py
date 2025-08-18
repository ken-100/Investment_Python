import pandas as pd
import bql
bq = bql.Service()



# Alternative to the BDP function
universe = ["IBM US Equity","AAPL US Equity"]
p_dates = bq.func.range("2025-8-1", "2025-8-4")
v_range = bq.func.range("2025-08-01","2025-08-10")

data_items = {
    "Name": bq.data.name(),
    "Crncy": bq.data.crncy(),
    "ISO": bq.data.country_iso(),
    "-5D": bq.data.px_last(dates="-5D"),
    "0801": bq.data.px_last(dates="2025-8-1"),
    "0804": bq.data.px_last(dates="2025-8-4"),
    "Ret%": bq.data.total_return(calc_interval=p_range),
    "Volume": bq.data.px_volume(dates=v_range).dropna().last(5).avg()
}

response = bq.execute(bql.Request(universe, data_items))

df = pd.concat(
    [data_item.df()[data_item.name] for data_item in response], 
    axis=1
)

df = df.reset_index(drop=False)
df

#                ID                            Name Crncy ISO     -5D    0801  \
# 0   IBM US Equity  International Business Machine   USD  US  240.07  250.05   
# 1  AAPL US Equity                       Apple Inc   USD  US  233.33  202.38   

#      0804      Ret%      Volume  
# 0  251.98 -0.118891   5575076.8  
# 1  203.35 -0.029911  86365256.2  



# Time series data
data_items = bq.data.px_last(dates=bq.func.range("-3D", '-1D'))
response = bq.execute(bql.Request(universe, data_items))

df = response[0].df()
df = df.reset_index(drop=False)
df

#                ID       DATE CURRENCY  PX_LAST(dates=RANGE(-3D,-1D))
# 0   IBM US Equity 2025-08-15      USD                         239.72
# 1   IBM US Equity 2025-08-16      USD                            NaN
# 2   IBM US Equity 2025-08-17      USD                            NaN
# 3  AAPL US Equity 2025-08-15      USD                         231.59
# 4  AAPL US Equity 2025-08-16      USD                            NaN
# 5  AAPL US Equity 2025-08-17      USD                            NaN



# fill=PREV
universe = ["IBM US Equity"]
data_items = bq.data.px_last(dates=bq.func.range("-8D", '-1D'),fill="PREV")
response = bq.execute(bql.Request(universe, data_items))

df = response[0].df()
df = df.reset_index(drop=False)
df



# TotalReturn
universe = ["IBM US Equity"]
data_items = bq.data.tot_return_index_gross_dvds(dates=bq.func.range("-5D", '-1D'),fill="PREV")
response = bq.execute(bql.Request(universe, data_items))

df = response[0].df()
df = df.reset_index(drop=False)
df


# Only Weekday for Total_Return
data_items = bq.data.tot_return_index_gross_dvds(dates=bq.func.range("-10D", '-1D'),Fill="Prev")
response = bq.execute(bql.Request(universe, data_items))

df = response[0].df()
df = df.reset_index(drop=True)

df.insert(1, 'DAY', df['DATE'].dt.strftime('%a'))
# df.drop(columns=["CURRENCY"], inplace=True)
df = df[~df["DAY"].isin(["Sun", "Sat"])]
df.columns = ["Date","Day","px_last"]
               
df



# Only Weekday
data_items = bq.data.px_last(dates=bq.func.range("-10D", '-1D'),Fill="Prev")
response = bq.execute(bql.Request(universe, data_items))

df = response[0].df()
df = df.reset_index(drop=True)

df.insert(2, 'DAY', df['DATE'].dt.strftime('%a'))
df.drop(columns=["CURRENCY"], inplace=True)
df = df[~df["DAY"].isin(["Sun", "Sat"])]

df.columns = ["Date","Day","px_last"]
df


# Historical data containing over two fields
p_dates = bq.func.range("-3D", "-1D")
data_items = {
    "date": bq.data.px_last(dates=p_dates)['DATE'],
    "px_last": bq.data.px_last(dates=p_dates),
    "px_volume": bq.data.px_volume(dates=p_dates)
}

response = bq.execute(bql.Request(universe, data_items))

df = pd.concat(
    [data_item.df()[data_item.name] for data_item in response],
    axis=1
)

df = df.reset_index(drop=True)
df
