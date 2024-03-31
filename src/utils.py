from datetime import datetime, timedelta

def get_minute(on_date=None, minutes_ago=0):
    now = datetime.now()
    if not on_date:
        return now.strftime("%Y-%m-%dT%H:%M:00Z")
    else:
        current_time = now.strftime("%H:%M")
        on_date_datetime = datetime.strptime(on_date, "%Y-%m-%dT%H:%M:%SZ")
        combined_datetime = datetime.combine(on_date_datetime, datetime.strptime(current_time, "%H:%M").time())
        return combined_datetime.strftime("%Y-%m-%dT%H:%M:00Z")
    
def get_day(days_ago=0):
    return (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%dT00:00:00Z")

def as_datetime(date):
    return datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")