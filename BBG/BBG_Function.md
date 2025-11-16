## Cheat Sheet


### BDH/Getting holiday *(any Ticker is available)*
```excel
=BDS("JPY BGN Curncy","CALENDAR_NON_SETTLEMENT_DATES","SETTLEMENT_CALENDAR_CODE=JN","CALENDAR_START_DATE=20220101","CALENDAR_END_DATE=20230101")

=BDS("JPY BGN Curncy","CALENDAR_NON_SETTLEMENT_DATES","SETTLEMENT_CALENDAR_CODE=JN US","CALENDAR_START_DATE=20220101","CALENDAR_END_DATE=20230101")

=@BDS("JPY BGN Curncy","CALENDAR_NON_SETTLEMENT_DATES","SETTLEMENT_CALENDAR_CODE=JN","CALENDAR_START_DATE="&TEXT(TODAY()-600,"yyyymmdd"),"CALENDAR_END_DATE="&TEXT(TODAY()+100,"yyyymmdd"))
```

Switzerland <br>
SZ: Natiolnal holiday<br>
BS: Basel Ex. (SIX Swiss)<br>
As for BS, there is a gap between settlement (default) and trading information. From BDS, we can only access settlement information.<br>


### Date of release of economic indicators
```excel
=@BDS("ADP CHNG Index","ECO_FUTURE_RELEASE_DATE_LIST", "START_DT=20000101", "END_DT=20200101")
```
- If you don't need the time `ECO_RELEASE_DT_LIST`

### BDH, weekday
Although the results are usually the same, depending on the ticker, the upper row includes Saturdays and Sundays.
```excel
=@BDH(C4,"px_last",WORKDAY(B2,-599),B2,"Days=W","Fill=P")
=@BDH(C4,"px_last",WORKDAY(B2,-599),B2,"CDR=5D","Fill=P")
```

can also specify national holidays.
```excel
=@BDH(C4,"px_last",WORKDAY(B2,-599),B2,"CDR=JN","Fill=P")
```

### Start date of time series data calculation
```excel
=INDEX(BDH("EMM US Equity", "px_last", "-20AY", "","array=t"), 1, 1)
=INDEX(BDH("EMM US Equity", "px_last", "20000101", "","array=t"), 1, 1)
=BQL("EMM US Equity","first(dropna(px_last(dates=range(-20y,0d))),1).date+0d")
=BQL("EMM US Equity","first(dropna(px_last(dates=range(2007-01-01,2023-09-29))),1).date+0d")
```

### Tick data
```excel
=BDH("TP1 Index","close,volume","2024/11/25  7:00:00","2024/11/26  7:00:00","BarTp=Trade","BarSz=30","TZ=Tokyo")
```

### Generic Ticker of futures
```excel
TY1 A:00_0_R COMB Comdty
```

### BQL
```excel
=@BQL(C5:C11,"total_return(Calc_interval=range(2025-05-26,2025-05-27))")
=@BQL(C5:C11,"last(tot_return_index_gross_dvds(dates=range(2025-06-18,2025-06-19),fill=PREV)).value/first(tot_return_index_gross_dvds(dates=range(2025-06-18,2025-06-19),fill=PREV)).value-1")
```

### Generic Ticker of futures
```excel
TY1 A:00_0_R COMB Comdty
```


### FXFORWARD
```excel
=BFXFORWARD("USDJPY","07/15/2025","BidPoints","PricingDate=06/25/2025")
=BFXFORWARD("USDJPY","07/15/2025","BidOutright","PricingDate=06/25/2025")
```
*HELP DAPI <GO> >> Specialized Toolkits >> BFXForward


### Update BBG function via VBA
```vba
Application.Run "RefreshCurrentSelection"
Application.Run "RefreshEntireWorksheet"
Application.Run "RefreshEntireWorkbook"
Application.Run "RefreshAllWorkbooks"
```

### Python pip
```bash
!pip install --index-url=https://bcms.bloomberg.com/pip/simple blpapi
!pip install pdblp
!pip install xbbg
```
