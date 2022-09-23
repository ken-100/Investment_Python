import workdays
import datetime
import calendar
from datetime import datetime, timedelta, date


# Input date
d1 = date(2022, 9, 1)
print("Input date :",d1)

# Today
d1 = date.today()
print("Today :",d1)

# Timde delta
tmp=5
d2 = d1 + timedelta(days=tmp)
print("Day+"+str(tmp)+" :",d2)
# Workday
d2 = workdays.workday(date.today(), days=5)
print("Workday+"+str(tmp)+" :",d2)

# Gap
d =d1 -d2
print("Gap :",d)
print("Gap_day :",d.days)
print("Gap_second :",d.seconds)

print("Foramt")
print(d1)
print(d1.strftime("%Y%m%d"))
print(d1.strftime("%y%m%d"))
print(d1.strftime("%Y%m"))
print(d1.strftime("%Y/%m/%d"))
print(d1.strftime("%Y/%m"))


# First of month
d = d1.replace(day=1)
print("First of month :",d)
# End of month
d = d1.replace(day=calendar.monthrange(d1.year, d1.month)[1])
print("End of the month :",d)

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


# Now -> Today
d1 = date(d.year, d.month, d.day)
d2 = d.replace(second=0).replace(hour=0).replace(minute=0).replace(second=0).replace(microsecond=0)

print("Now -> Today :",d1)
print("Now -> Today :",d2)

d1 = '20210501'
d2 = datetime.strptime(d1, '%Y%m%d')

print("String :",d1)
print("datetime :",d2)


# Excel figure -> date
tmp = 44827
d = datetime(1899, 12, 30) + timedelta(days=tmp)
print("Excel figure :",tmp)
print("datetime :",d)
