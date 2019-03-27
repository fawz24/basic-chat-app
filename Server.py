# -*- coding: utf-8 -*-

import flask

app = flask.Flask(__name__)

@app.route('/')
def hello_world():
    return 'Welcome to the chat app!'


#with app.test_request_context():
#    print(flask.url_for('hello_world'))
#    print(flask.url_for('show_path', subpath=r'c:\test', redirect='home'))
#    print(flask.url_for('projects'))