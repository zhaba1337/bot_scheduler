import sqlite3



def create_connect():
    con = sqlite3.connect("db.sqlite3")
    cur = con.cursor()
    
    return (con, cur)

def close_connect(con):
    con.commit()
    con.close()


def add_datetime_slot():
    con, cur = create_connect()

    cur.execute('insert into Datetime_slots()')
    
    close_connect(con)

def main():
    import calendar
    import datetime
    con, cur = create_connect()

    
    busy_time_slots = cur.execute("""select * from Datetime_slots 
                                  join Records ON Records.datetime_slot_id = Datetime_slots.id and date_with_timezone = ?
                                  """, ('2024-08-08',)).fetchall()
   
   
    close_connect(con)




#request for get busy_days in interval 
# select * from (SELECT date_with_timezone from Datetime_slots
# GROUP BY date_with_timezone
# HAVING count(date_with_timezone) = 4) as q
# where (date_with_timezone BETWEEN "2024-08-11" and "2024-08-31")



if __name__ == '__main__':
    main()
    
