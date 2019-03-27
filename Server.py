# -*- coding: utf-8 -*-

import flask
import flask_socketio

app = flask.Flask(__name__)
app.secret_key = b'\xf8\xd90\xd9\xb7\xb6\\\xee\xa0\x84\xe9d@\x9f%\xd4'
socketio = flask_socketio.SocketIO(app)

@app.route('/')
def hello_world():
    return flask.render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    if flask.request.method == 'POST':
        flask.request.form['nickname']

@socketio.on('simple message')
def handle_simple_message(message):
    print('Simple message received: ' + message)

@socketio.on('group message')
def handle_group_message(message):
    print('Group message received: ' + message)

@socketio.on('broadcast message')
def handle_broadcast_message(message):
    print('Broadcast message received: ' + message)
    
@socketio.on('new group')
def handle_new_group(info):
    print(f'New group created: name={info.name} creator={info.creator}')

if __name__ == '__main__':
    socketio.run(app)
