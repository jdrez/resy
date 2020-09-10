import helpers.logger

import boto3
import json
import os

log = helpers.logger.Logger(__name__)


CONFIG = None

def refresh():
    global CONFIG
    client = boto3.client('secretsmanager')
    CONFIG = json.loads(client.get_secret_value(SecretId=f"resy")['SecretString'])
    log.info("refresh", config=CONFIG)

def get(key):
    try:
        value = json.loads(CONFIG[key])
    except ValueError:
        value = CONFIG[key]
    return value
