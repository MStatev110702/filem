from datetime import datetime, timedelta
from calendar import monthrange
from ..entities.enums import IntervalTypeComboValues

def calculate_next_run(interval_type: str, schedule_type: str, schedule_value: int) -> datetime:
    if interval_type == "interval":
        return calculate_interval(IntervalTypeComboValues[schedule_type].value, schedule_value)
    elif interval_type == "date/time":
        return calculate_date_time(schedule_type, schedule_value)
    
def calculate_interval(schedule_type: str, schedule_value: int) -> datetime:
    return datetime.now() + timedelta(**{schedule_type: schedule_value})

def calculate_date_time(time: str, schedule_value: int) -> datetime:
    now = datetime.now()
    year = now.year
    month = now.month

    t = datetime.strptime(time, "%H:%M")
    hour = t.hour
    minute = t.minute

    last_day = monthrange(year, month)[1]
    actual_day = min(schedule_value, last_day)

    next_date = datetime(year, month, actual_day, hour, minute) 

    if next_date > now:
        return next_date
    
    if month == 12:
        year += 1
        month = 1
    else:
        month += 1

    last_day = monthrange(year, month)[1]
    actual_day = min(schedule_value, last_day)

    return datetime(year, month, actual_day, hour, minute)