# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START app]
import logging
from flask import Flask, jsonify, request
import translation as tr 

app = Flask(__name__)


@app.route('/send', methods=['POST'])
def send():
    req_json = request.get_json(force=True, cache=False)
    
    # firebase send logic here
    response = dict()
    try:
        receiverId = req_json['receiverId']
        senderId = req_json['senderId']
        
        dest_lang = tr.get_dest_lang({'uid': [receiverId]})
        msg_text = req_json['msg'] 
        translated = tr.translate_text(dest_lang, msg_text)

        send_data = {
            'msg': translated['text'],
            'timestamp': int(req_json['timestamp']),
            'userid': receiverId
        }

        tr.firebase_send(senderId, receiverId, send_data)

        response['status'] = True
        response['message'] = 'Message sent'
  
    except Exception as e:
        response['status'] = False
        response['message'] = str(e)

    return jsonify(response)


@app.route('/user/add', methods=['POST'])
def add_user():
    req_json = request.get_json(force=True, cache=False)
    uid = req_json['uid']
    email = req_json['email']
    data = req_json['data']
    response = tr.add_user(uid, email, data)
    return jsonify(response)

@app.route('/user/update', methods=['PUT'])
def update_user():
    req_json = request.get_json(force=True, cache=False)
    email = req_json['email']
    data = req_json['data']
    response = tr.update_user(email, data)
    return jsonify(response)

@app.route('/user/get', methods=['GET'])
def get_user():
    filters = dict(request.args)
    response = tr.get_user(filters)
    return jsonify(response)

@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception(e)
    return 'An internal error occurred.', 500
# [END app]
