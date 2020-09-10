import datetime
import pytz


est = pytz.timezone('America/New_York')

def parse_firebase(dt):
    dt = str(dt.astimezone(est))
    return datetime.datetime.strptime(dt, '%Y-%m-%d %H:%M:%S%z')

def missed(dt):
    now = datetime.datetime.now().astimezone(est)
    return now > dt

def date_resy(dt):
    return dt.strftime('%Y-%m-%d')

def datetime_resy(dt):
    return dt.strftime('%Y-%m-%d %H:%M:%S')
