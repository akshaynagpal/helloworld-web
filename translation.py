from google.cloud import translate, datastore
import google.auth
import json
import pyrebase
import json
import logging

FIREBASE_CONFIG = None
with open('keys/firebase-secrets.json') as f:
    FIREBASE_CONFIG = json.load(f)

class DataStore(object):
    def __init__(self, project_id):
        self.client = datastore.Client(project_id)

    def add_user(self, uid, email, data):
        response = dict()
        try:
            key = self.client.key('user', str(email))
            user = datastore.Entity(key)
            user['uid'] = str(uid)
            for key in data:
                user[key] = data[key]
            self.client.put(user)

            response['status'] = True
            response['message'] = 'User added successfully'
        except ValueError as e:
            response['status'] = False
            response['message'] = str(e)

        return response

    def update_user(self, email, data):
        response = dict()
        try:
            with self.client.transaction():
                key = self.client.key('user', email)
                user = self.client.get(key)

                if not user:
                    raise ValueError('User does not exist')

                for key in data:
                    user[key] = data[key]
                self.client.put(user)

                response['status'] = True
                response['message'] = 'User updated successfully'
        
        except ValueError as e:
             response['status'] = False
             response['message'] = str(e)

        return response

    def get_user(self, filters):
        response = dict()
        query = self.client.query(kind='user')
        for key in filters:
            for val in filters[key]:
                query.add_filter(key, '=', val)
        results = list(query.fetch())
        return results



def add_user(uid, email, data=dict()):
    credentials, project_id = google.auth.default()
    ds_client = DataStore(project_id)
    return ds_client.add_user(uid, email, data)


def update_user(email, data):
    credentials, project_id = google.auth.default()
    ds_client = DataStore(project_id)
    return ds_client.update_user(email, data)

def get_user(filters):
    credentials, project_id = google.auth.default()
    ds_client = DataStore(project_id)
    return ds_client.get_user(filters)

def translate_text(target_lang, text):
    # Translates text into the target language.
    # Target must be an ISO 639-1 language code.
    # See https://g.co/cloud/translate/v2/translate-reference#supported_languages

    credentials, project_id = google.auth.default()
    translate_client = translate.Client(credentials=credentials)

    logging.info(target_lang)
    logging.info(text)
    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.translate(text, target_language=target_lang)

    response = dict()
    if isinstance(result, dict):
        response['text'] = result['translatedText']
    elif isinstance(result, list):
        response['text-lines'] = list()
        for item in result:
            response['text-lines'].append(item['translatedText'])
    
    return response

def get_dest_lang(user_data):
    user = get_user(user_data)
    return user[0]['pref-lang']
 
def firebase_send(senderId, receiverId, send_data):
    FIREBASE = pyrebase.initialize_app(FIREBASE_CONFIG)
    FIREBASE_DB = FIREBASE.database()
    FIREBASE_DB.child("%s/%s" % (receiverId, senderId)).push(send_data)
