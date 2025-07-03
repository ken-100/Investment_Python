import bql
bq = bql.Service()
u = bq.univ
d = bq.data
f = bq.func

ticker = 'nky index'
dt = f.range('-1m', '-1d')



data = {
    'price': d.px_last(dates=dt).dropna(),
}
req = bql.Request(ticker, data, preferences=dict(dropcols=['currency']))
res = bq.execute(req)
df = bql.combined_df(res)
df = df.reset_index(drop=True)
df.columns = ["Date","Price"]

display(df.head())


data = {
     'eps': d.headline_eps_market(fpt='a', ae='e', fpo='1', dates=dt).dropna(),
}
req = bql.Request(ticker, data, preferences=dict(dropcols=['as_of_date', 'currency', 'PERIOD_END_DATE']))
res = bq.execute(req)
df1 = bql.combined_df(res)
df1 = df1.reset_index(drop=True)
df1.columns = ["Date","EPS"]
display(df1.head())

df["EPS"] = df["Date"].map(df1.set_index("Date")["EPS"])
df.head()
