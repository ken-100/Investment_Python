## Bloomberg Functions Cheat Sheet

### Overview
| Abbreviation | Description                          |
|--------------|--------------------------------------|
| WEI          | World Equity Indices                 |
| WEIF         | World Index Futures                  |
| EMEQ         | Emerging Market Equity Indices       |
| WB           | World Bond Market                    |
| WBI          | World Inflation Bond                 |
| WBF          | World Bond Futures                   |
| WIR          | World Interest Rate Futures          |
| FICM         | Fixed Income Credit Monitor          |
| WCDS         | World CDS Monitor                    |
| CDX          | CDS Index Monitor                    |
| SOVR         | Sovereign CDS Monitor                |
| GGR          | Generic Government Rates (*Obsolete*)|
| SOVM         | Sovereign Debt Monitor               |
| IRSB         | Interest Rate Swap                   |
| USSW         | Swap Market (US)                     |
| GLCO         | Global Commodity Prices              |
| CSDR         | Sovereign Ratings                    |
| ETF          | ETF                                  |
| GMM          | Global Macro Movers                  |
| OTC          | Market Monitor                       |
| WCR          | World Currency Rates                 |
| BTMM         | Treasury & Money Markets             |
| DMMV         | Developed Markets Summary            |
| EMMV         | Emerging Markets Summary             |

### Policy Rate & Inflation
| Abbreviation    | Description                          |
|-----------------|--------------------------------------|
| IFMO            | Inflation Monitor                    |
| MIPR            | Market Implied Policy Rates          |
| WIRP            | World Interest Rate Probability      |
| BECO            | Bloomberg Economics                  |
| DOTS            | FOMC Dot Plot                        |
| DOTS SPEC       | Dot + Fed Spectrometer               |
| .3M6MHD  Index  |                                      |
| .6M12MHD  Index |                                      |
| BENLPFED  Index |                                      |
| MSRAUS  Index   |                                      |

### News
| Abbreviation | Description                          |
|--------------|--------------------------------------|
| DS           | Document Search                      |
| N, NI        | News Topics (*e.g., NI BOJ*)         |
| TOP, TOPJ    | Top News                             |
| TLIV         | Top Live Blogs                       |
| MILV         | Market Live Blog                     |
| LIVE         | Live                                 |
| DAYB         | DayBreak                             |
| BTDY         | Bloomberg Today                      |
| READ, JREAD  | Most Read Stories                    |
| CVID         | Covid                                |
| ALRT         | Alerts Manager                       |
| FRNT         | Front                                |
| MLIV         | Market Live                          |
| FIRS         | First Word                           |
| MEDI         | Media (BBG TV, Radio)                |
| MEDI LIVE    | Media Live                           |
| MREP         | Morning Report                       |
| NSUB         | News Subscriptions                   |
| NT           | News Trends Chart                    |
| NSTM         | Key News Themes                      |
| JIJI         | JIJI Press                           |
| AID          | Automated Intelligence on Demand     |
| BNEW         | What's New                           |

### Economic
| Abbreviation | Description                          |
|--------------|--------------------------------------|
| ECO          | Economic Calendars                   |
| ECFC         | Forecasts                            |
| ECST         | World Economic Statistics            |
| ECOD         | Economic Release Details             |
| ECWB         | Economic Workbench                   |
| ECAN         | World Economic Analyzer              |
| FCON         | Financial Conditions                 |
| ESCU         | Economic Surprises                   |
| TAYL         | Taylor Rule Model                    |
| BECO         | Bloomberg Economics (Visual Charts)  |

### Futures
| Abbreviation | Description                          |
|--------------|--------------------------------------|
| OMON         | Option Monitor                       |
| COT          | CFTC Ticker                          |
| PCS          | Commodity Defaults                   |
| MDM          | Market Depth Monitor                 |
| EXC          | Exchange Privileges                  |

### Equities (including ETF)
| Abbreviation | Description                          |
|--------------|--------------------------------------|
| AQR          | Top Trade                            |
| QR           | Quote Recap                          |
| QM           | Quote Montage                        |
| TSM          | Trade Summary Matrix                 |
| MBTRR        | Monitoring Block Trade Recap         |
| VBAR         | Volume Dimension Bars                |
| HP, HCP, HCPI| Historical Price & OHLC Tables       |
| OMON         | Option Monitor                       |
| CACS         | Corporate Action                     |
| CN           | Corporate News                       |
| SI           | Short Interest                       |
| Rank         | Broker Rankings                      |
| MRR          | Members Ranked Return                |
| DPDF         | Corporate Action Settings            |
| KI           | Insight                              |

### ETF
| Abbreviation | Description                          |
|--------------|--------------------------------------|
| ETF          |                                      |
| HLDR         | Holder Ownership                     |
| Port         |                                      |


### Stock Index Analysis
| Abbreviation | Description                          |
|--------------|--------------------------------------|
| IMAP         | Intraday Market Map                  |
| MEMB         | Member Weight                        |
| GRR          | Group Ranked Returns                 |

### BI Strategy
- EVTS ER, BI STOXN SPXERNT, BI STOXG CHINA, SPX Index EA

### Bonds, Swap
- NIM, CRV, CRVF, FWCM, FWCV

### FX, Currency
- CSBSUSD, MSFXJPY Index, USDJPYTL, USDJPYCR

### Commodity
- CPFC, Line, NRGZ, BI EXPRE JODIP, RIG, WFOR, COMM, COM US Equity

### Monitoring
- GMM, W (Security Worksheet)

### AI
- AIBB

### Charts, Graphs, Calculations
- G, GP, GPC, GIP, GY, GIY, RRG, CORR, CIX, SEAG, COMP, TRA, GR, HS

### BackTest & Factor Analysis
- BTST, FTW, FTW FRR, BQIQ

### Operation
- CLIP, GRIB, GRAB, SNIP, Shift + G

### Template & Documents
- XLTP, DOCS, SMNR, BQLX, BPS, HELP, TRAI

### Excel & Bloomberg formulas
- BDH, BDS, BQL formulas

### Python
- Bloomberg pip packages (`blpapi`, `pdblp`, `xbbg`)

### Twitter
- SOCI (usernames: @zerohedge, @nicktimiraos, etc.)

### Profile & Launchpad
- IAM, MYOR, BLP, LLP

Here's the content converted into Markdown format:

## Bonds, Swap
| Code  | Description                |
|-------|----------------------------|
| NIM   | New Issue Monitor          |
| CRV   | Custme Curve Builder       |
| CRVF  | Curve Filter               |
| FWCM  | Forward Curve Matrix       |
| FWCV  | Forward Curve Analysis     |

## FX, Currency
| Code              | Description                   |
|-------------------|-------------------------------|
| CSBSUSD TMUQ Curncy | Mitsubishi ttm              |
| CSBSUSD STBJ Curncy | SumiTrust ttm               |
| MSFXJPY Index       | WM/Refinitiv                |
| USDJPYTL Curncy     | Total Return Long           |
| USDJPYCR Curncy     | Carry Return                |

## Commodity
| Code | Description                        | Notes                                  |
|------|------------------------------------|----------------------------------------|
| CPFC | Commodity Price Forecasts          | Future Price, Forecasts from Broker    |
| Line | Global Commodity Flows             |                                        |
| NRGZ | Energy Industry Reports            |                                        |
| BI   | EXPRE JODIP                        |                                        |
| RIG  | Rig Count                          |                                        |
| WFOR | Weather Forecasts                  |                                        |
| COMM | Commodity Product Catalog          |                                        |

