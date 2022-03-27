from xbbg import blp
import workdays
import datetime

# d_from = "20050301"
d_from = workdays.workday(datetime.datetime.today(), days=-260).strftime("%Y%m%d")
d_to = workdays.workday(datetime.datetime.today(), days=-1).strftime("%Y%m%d")

US = blp.bds("JPY Curncy","CALENDAR_NON_SETTLEMENT_DATES", CALENDAR_START_DATE=d_from, CALENDAR_END_DATE=d_to,SETTLEMENT_CALENDAR_CODE="US")
US
