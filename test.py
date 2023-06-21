import datetime

current_date = datetime.datetime.now()
a = int(current_date.strftime("%Y%m%d%H%M%S"))

print(a)    