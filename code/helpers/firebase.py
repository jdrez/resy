import helpers.config

import firebase_admin
from firebase_admin import firestore


DB = None

def init():
    global DB
    gcp_token = helpers.config.get('gcp.token')
    credentials = firebase_admin.credentials.Certificate(gcp_token)
    firebase_admin.initialize_app(credentials)
    DB = firestore.client()

def scheduled():
    return DB.collection('scheduled').stream()
