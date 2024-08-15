from datetime import datetime
import pytz

def fomart_time_to_vn(time):
    if isinstance(time, datetime):
        utc_time = time
    else:
        utc_time = datetime.strptime(time, '%Y-%m-%d %H:%M:%S%z')
    vietnam_tz = pytz.timezone('Asia/Ho_Chi_Minh')
    vietnam_time = utc_time.astimezone(vietnam_tz)
    return vietnam_time