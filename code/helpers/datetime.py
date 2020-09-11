import datetime
import pytz


nytz = pytz.timezone('America/New_York')

def parse_firebase(dt):
    return datetime.datetime.strptime(str(dt.astimezone(nytz)), '%Y-%m-%d %H:%M:%S%z')

def parse_resy(dt):
    return nytz.localize(datetime.datetime.strptime(dt, '%Y-%m-%d %H:%M:%S'))

def missed(dt):
    return datetime.datetime.utcnow().astimezone(nytz) > dt

def date_resy(dt):
    return dt.strftime('%Y-%m-%d')
