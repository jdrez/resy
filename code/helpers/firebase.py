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

def reserve():
    return DB.collection('reserve').get()

def booked(document_id, document):
    DB.collection('booked').document(document_id).set(document)
    DB.collection('reserve').document(document_id).delete()

def missed(document_id, document):
    DB.collection('missed').document(document_id).set(document)
    DB.collection('reserve').document(document_id).delete()


init()
