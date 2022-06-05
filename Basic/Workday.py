import workdays
import datetime
d = workdays.workday(datetime.datetime.today(), days=-1).strftime("%Y%m%d")
d
