import sqlite3
from dataclasses import dataclass
from typing import List, Any



@dataclass
class DB_connector:
    con: sqlite3.Connection = sqlite3.connect("db.sqlite3")
    cur: sqlite3.Cursor = con.cursor()
    
    def get_time_slots(self) -> List[str]:
        return [f"{i[0]}:00-{i[1]}:00" for i in self.cur.execute('select start_at, end_at from Time_slots').fetchall()]

    def get_user_name(self, user_id: int) -> str:
        return self.cur.execute('SELECT first_name FROM Clients WHERE telegram_id = ?', (user_id,)).fetchone()[0]
    
    def get_telegram_id(self, username: str) -> int: 
        return self.cur.execute('select telegram_id from Clients WHERE first_name = ?', (username,)).fetchone()[0]
    
    def get_owner_id(self) -> int:
        return self.cur.execute('select telegram_id from Owners').fetchone()[0]
    
    def get_owner_username(self) -> str:
        return self.cur.execute('select username from Owners').fetchone()[0]
    
    def insert_record(self, client_id, datetime_slot_id, time_slot):
        self.cur.execute(
            """INSERT INTO Records (client_id, datetime_slot_id, is_weekend) 
                VALUES (
                    (SELECT id from Clients where telegram_id = ?),
                    (SELECT id FROM Datetime_slots WHERE date_with_timezone = ? AND time_slot_id = ?),
                    0)
            """, 
            (client_id, datetime_slot_id, time_slot))
        self.con.commit()
    
    def get_all_books(self) -> List[Any]:
         return self.cur.execute(
            """SELECT Clients.first_name, Datetime_slots.date_with_timezone, Time_slots.start_at, Time_slots.end_at FROM Records
            JOIN Clients ON Clients.id = Records.client_id
            JOIN Datetime_slots ON Datetime_slots.id = datetime_slot_id
            JOIN Time_slots ON Datetime_slots.time_slot_id = Time_slots.id
            ORDER BY Datetime_slots.date_with_timezone, start_at DESC"""
        ).fetchall()
    
    def get_client_books(self, telegram_id: int) -> List[Any]:
        return self.cur.execute(
            """SELECT Datetime_slots.date_with_timezone, Time_slots.start_at, Time_slots.end_at FROM Records
            JOIN Clients ON Clients.id = Records.client_id and Clients.telegram_id = ?
            JOIN Datetime_slots ON Datetime_slots.id = datetime_slot_id
            JOIN Time_slots ON Datetime_slots.time_slot_id = Time_slots.id
            ORDER BY Datetime_slots.date_with_timezone, start_at DESC"""
        , (telegram_id, )).fetchall()
        
        
    
    def close_connection(self) -> None:
        self.con.commit()
        self.cur.close()
        self.con.close()


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
    connector = DB_connector()
    
    connector.insert_record(8, 2, 1)


#request for get busy_days in interval 
# select * from (SELECT date_with_timezone from Datetime_slots
# GROUP BY date_with_timezone
# HAVING count(date_with_timezone) = 4) as q
# where (date_with_timezone BETWEEN "2024-08-11" and "2024-08-31")



if __name__ == '__main__':
    main()
    
