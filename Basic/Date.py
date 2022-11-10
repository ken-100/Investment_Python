import workdays
import datetime
import calendar
from datetime import datetime, timedelta, date


# Input date
d1 = date(2022, 9, 1) 
print("Input date :",d1)
# Input date : 2022-09-01


# Today
d1 = date.today()
print("Today :",d1)
# Today : 2022-09-30


# Timde delta
tmp=5
d2 = d1 + timedelta(days=tmp)
print("Day+"+str(tmp)+" :",d2)
# Day+5 : 2022-10-05

# Workday
d2 = workdays.workday(date.today(), days=5)  
print("Workday+"+str(tmp)+" :",d2)
# Workday+5 : 2022-10-07

#Sat, Sun -> Weekday
d3 = date(2007, 3, 31)
d3 = workdays.workday(d3+timedelta(days=1), days=-1)
print(d3)
# 2007-03-30

from dateutil.relativedelta import relativedelta
d3 = d3 + relativedelta(months=3)
print(d3)
# 2007-06-30

d3 = d3 + relativedelta(years=3)
print(d3)
# 2010-06-30

# Gap
d =d1 -d2
print("Gap :",d)
print("Gap_day :",d.days)
print("Gap_second :",d.seconds)
# Gap : -7 days, 0:00:00
# Gap_day : -7
# Gap_second : 0


print("Foramt")
print(d1)
print(d1.strftime("%Y%m%d"))
print(d1.strftime("%y%m%d"))
print(d1.strftime("%Y%m"))
print(d1.strftime("%Y/%m/%d"))
print(d1.strftime("%Y/%m"))
# Foramt
# 2022-09-30
# 20220930
# 220930
# 202209
# 2022/09/30
# 2022/09

# First of month
d = d1.replace(day=1)
print("First of month :",d)
# First of month : 2022-09-01

# End of month
d = d1.replace(day=calendar.monthrange(d1.year, d1.month)[1])
print("End of the month :",d)
# End of the month : 2022-09-30

# Now
d =datetime.now()
print("Now :",d)
print("year :",d.year)
print("month :",d.month)
print("day :",d.day)
print("hour :",d.hour)
print("minute :",d.minute)
print("second :",d.second)
print("microsecond :",d.microsecond)
# Now : 2022-09-30 17:23:21.789900
# year : 2022
# month : 9
# day : 30
# hour : 17
# minute : 23
# second : 21
# microsecond : 789900

# Now -> Today
d1 = date(d.year, d.month, d.day)
d2 = d.replace(second=0).replace(hour=0).replace(minute=0).replace(second=0).replace(microsecond=0)
print("Now -> Today :",d1)
print("Now -> Today :",d2)
# Now -> Today : 2022-09-30
# Now -> Today : 2022-09-30 00:00:00
            
d1 = '20210501'
d2 = datetime.strptime(d1, '%Y%m%d')
print("String :",d1)
print("datetime :",d2)
# String : 20210501
# datetime : 2021-05-01 00:00:00

# Excel figure -> date
tmp = 44827
d = datetime(1899, 12, 30) + timedelta(days=tmp)
print("Excel figure :",tmp)
print("datetime :",d)
# Excel figure : 44827
# datetime : 2022-09-23 00:00:00
