import sqlite3



def create_connect():
    con = sqlite3.connect("db.sqlite3")
    cur = con.cursor()
    
    return (con, cur)

def close_connect(con):
    con.commit()
    con.close()

def main():
    con, cur = create_connect()
    time_slots = []
    for i in range(1, 5):
        time_slots.append(('2024-08-18', i))
        
    con.executemany( 
        """INSERT INTO Records (client_id, datetime_slot_id, is_weekend) 
            VALUES (?, ?, ?)""", [(6, i[0], 1) for i in cur.execute('select id from Datetime_slots order by id desc limit 4').fetchall()]
            )
    close_connect(con)

#request for get busy_days in interval 
# select * from (SELECT date_with_timezone from Datetime_slots
# GROUP BY date_with_timezone
# HAVING count(date_with_timezone) = 4) as q
# where (date_with_timezone BETWEEN "2024-08-11" and "2024-08-31")



if __name__ == '__main__':
    main()
    
