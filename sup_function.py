from datetime import date, timedelta,datetime



def prev_month(current_month):
    return current_month.replace(day=1) - timedelta(days=1)


def next_month(current_month):
    return (current_month.replace(day=1) + timedelta(days=32)).replace(day=1)



