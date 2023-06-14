from pytrends.request import TrendReq
import pandas as pd
# https://github.com/GeneralMills/pytrends
# https://qiita.com/takubb/items/e5578a8143a4f6b0f7fc

pytrends = TrendReq(hl='en-US', tz=360, timeout=(100,200) ) 
KW = ["Bitcoin","Covid"]
for i in range(len(KW)):
#     pytrends.build_payload([KW[i]], timeframe="today 1-m", geo='US')
    pytrends.build_payload([KW[i]], timeframe="now 7-d", geo='US')
    tmp = pytrends.interest_over_time()
    if i == 0:
        df = tmp.iloc[:,:1]
    else:
        df = pd.concat([df, tmp.iloc[:,0:1]], axis=1)
    
df = df.sort_index(ascending=False)
df
