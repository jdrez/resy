import datetime
import pytz


def parse_firebase(dt):
    dt = str(dt.astimezone(pytz.timezone('America/New_York')))
    return datetime.datetime.strptime(dt, '%Y-%m-%d %H:%M:%S%z')

def date_resy(dt):
    return dt.strftime('%Y-%m-%d')

def datetime_resy(dt):
    return dt.strftime('%Y-%m-%d %H:%M:%S')
