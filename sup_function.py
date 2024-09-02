


from datetime import timedelta
def prev_month(current_month):
    return current_month.replace(day=1) - timedelta(days=1)


def next_month(current_month):
    return (current_month.replace(day=1) + timedelta(days=32)).replace(day=1)



from aiogram import types
from db import * 
import emoji
def create_calendar(obj, builder, current_year, current_month, cb, cb_text='choice_time_slot'):
    con, cur = create_connect()
    busy_days = [i for j in cur.execute(f"""
                select strftime('%d', date_with_timezone) from (SELECT date_with_timezone from Records
                join Datetime_slots ON datetime_slot_id = Datetime_slots.id
                GROUP BY strftime("%d", date_with_timezone)
                HAVING count(date_with_timezone) = 4) as q
                where (date_with_timezone BETWEEN ? and date(?, '-1 days', '+1 month'))                      
                """, 
                (f"{current_year}-{str(current_month).zfill(2)}-01", 
                f"{current_year}-{str(current_month).zfill(2)}-01")
                ).fetchall() for i in j]

    print(busy_days)
    for i in obj:
        builder1  = []
        for j in i:
            data, for_callback = '-', '-'
            if(j[0]):
                
                data = str(j[0])
                for_callback = cb(name=cb_text, date=f"{current_year}-{str(current_month).zfill(2)}-{str(j[0]).zfill(2)}").pack()

                
            if (data.zfill(2) in busy_days):
                data = emoji.emojize(":cross_mark:")
                for_callback = 'empty'
                
            builder1.append(types.InlineKeyboardButton(
                text= data,
                callback_data = for_callback)
            )
        
        builder.row(*builder1)
    
    return builder