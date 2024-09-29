#from sup_function import * 
from datetime import datetime, timedelta
import calendar
from db import DB_connector
from dateutil.relativedelta import relativedelta

import re 
# x^2-10x+4
m = [4, -10, 1]
dx_dm = []
counter = 1
for i in m[1:]:
    dx_dm.append(i*counter)
    counter += 1
    
print(dx_dm)