import pdblp
from xbbg import blp
import workdays
import time
import pandas as pd
pd.set_option('display.max_columns', 70)

d_from = "20050301"
d_to = workdays.workday(datetime.datetime.today(), days=-1).strftime("%Y%m%d")


# tmp = con.bdh("ES1 Index", "px_last", d_from, d_to,
#              elms = [("periodicitySelection", "MONTHLY")]).reset_index()

# tmp = con.bdh("ES1 Index", "px_last", d_from, d_to,
#              elms = [("periodicitySelection", "WEEKLY")]).reset_index()

tmp = con.bdh("ES1 Index", "px_last", d_from, d_to,
             elms = [("periodicitySelection", "QUARTERLY")]).reset_index()

tmp

# DAILY
# WEEKLY
# MONTHLY
# QUARTERLY
# SEMI_ANNUALLY
# YEARLY

# https://data.bloomberglp.com/labs/sites/2/2013/12/blpapi-developers-guide-1.38.pdf
# https://data.bloomberglp.com/professional/sites/10/2017/03/BLPAPI-Core-Developer-Guide.pdf
