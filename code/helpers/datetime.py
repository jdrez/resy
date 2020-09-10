import datetime
import pytz


est = pytz.timezone('America/New_York')

def parse_firebase(dt):
    return datetime.datetime.strptime(str(dt.astimezone(est)), '%Y-%m-%d %H:%M:%S%z')

def parse_resy(dt):
    return datetime.datetime.strptime(dt, '%Y-%m-%d %H:%M:%S').astimezone(est)

def missed(dt):
    return datetime.datetime.now().astimezone(est) > dt

def date_resy(dt):
    return dt.strftime('%Y-%m-%d')
