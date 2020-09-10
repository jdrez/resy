import helpers.datetime
import helpers.logger

import json
import os
import requests

log = helpers.logger.Logger(__name__)


USER = None

def _write(filename, data):
    if 'LAMBDA_TASK_ROOT' not in os.environ:
        with open(f"./scratch/{filename}.json", 'w') as f:
            json.dump(data, f)

def _headers():
    api_key = helpers.config.get('resy.api_key')
    auth_token = (USER and USER['token']) or None
    return {
        'Accept': "application/json, text/plain, */*",
        'Authorization': f"ResyAPI api_key=\"{api_key}\"",
        'Cache-Control': "no-cache",
        'Connection': None,
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
        'x-origin': "https://resy.com",
        'x-resy-auth-token': auth_token,
    }

def _get(url, params={}):
    r = requests.get(url, headers=_headers(), params=params)
    if 'LAMBDA_TASK_ROOT' not in os.environ:
        log.info("_get", request_headers=r.request.headers)
    return json.loads(r.content)

def _post(url, data={}):
    r = requests.post(url, headers=_headers(), data=data)
    if 'LAMBDA_TASK_ROOT' not in os.environ:
        log.info("_post", request_headers=r.request.headers)
    response = json.loads(r.content)
    return response

def login(email, password):
    global USER
    data = {
        'email': email,
        'password': password,
    }
    response = _post("https://api.resy.com/3/auth/password", data)
    _write('user', response)
    USER = response

def find(date, venue_id, party_size):
    params = {
        'day': helpers.datetime.date_resy(date),
        'venue_id': venue_id,
        'party_size': party_size,
        'lat': 0,
        'long': 0,
    }
    response = _get(f"https://api.resy.com/4/find", params)
    _write('find', response)
    return response['results']['venues']

def details(config_token, date, party_size):
    params = {
        'config_id': config_token,
        'day': helpers.datetime.date_resy(date),
        'party_size': party_size,
    }
    response = _get(f"https://api.resy.com/3/details", params)
    _write('details', response)
    return response

def book(book_token):
    data = {
        'book_token': book_token,
    }
    response = _post("https://api.resy.com/3/book", data)
    return response

def valid_slots(date, slots):
    valid_slots = [s for s in slots if abs((helpers.datetime.parse_resy(s['date']['start']) - date).total_seconds()) <= 60 * 30]
    def sort(s):
        s_date = helpers.datetime.parse_resy(s['date']['start'])
        s_diff = abs((s_date - date).total_seconds())
        return (s_diff, s_date)
    valid_slots.sort(key=sort)
    return valid_slots
