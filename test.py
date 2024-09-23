#from sup_function import * 
from datetime import datetime, timedelta
import calendar
from db import DB_connector
from dateutil.relativedelta import relativedelta

today = datetime.now().date()

day = ((today + timedelta(days=62)).replace(day=today.day))

while(today <= day):
    print(today)
    today += timedelta(days=1)