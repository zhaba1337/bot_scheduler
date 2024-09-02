#from sup_function import * 
from datetime import datetime, timedelta
import calendar
from db import DB_connector



print(DB_connector().get_client_books(5005348535))