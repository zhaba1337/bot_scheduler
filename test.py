from sup_function import * 
from datetime import datetime
month = 11
year = 2024

date = datetime(year, month, 1, 0, 0)


print(next_month(date).month)