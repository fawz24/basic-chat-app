# -*- coding: utf-8 -*-

import datetime
import uuid
import hashlib
import flask.sessions as sessions
import helpers

class User:
    """User defines a simple user in the chat"""
    def __init__(self, nick_name, password, groups=None):
        h = hashlib.sha256()
        h.update(password.encode())
        self.nick_name = nick_name
        self.password = h.hexdigest()
        self.groups = groups if groups else []
        
    def compare(self, user):
        """Compares the nick_name and password fields of the current instance object and another instance object"""
        if self.nick_name != user.nick_name:
            return False
        if self.password != user.password:
            return False
        return True
        
class Message:
    """The Message class represents a message sent and received in a chat"""
    def __init__(self, receiver, sender, content, ms_type='simple', date=None):
        self.receiver = receiver
        self.sender = sender
        self.content = content
        self.type = ms_type
        self.date = date if date else datetime.datetime.now()

class Group:
    """Group is a representation of a chat group"""
    def __init__(self, name, creator, participants=None, date=None, reference=None):
        self.name = name
        self.creator = creator
        self.participants = participants if participants != None else [creator]
        self.date = date if date else datetime.datetime.now()
        self.reference = reference if reference else len(self.participants)
        
    def compare(self, group):
        """Compare the name and creator fields of the current instance object to another instance object's same fields"""
        if self.name != group.name:
            return False
        if self.creator != group.creator:
            return False
        return True
    
class MongoSession(sessions.CallbackDict, sessions.SessionMixin):
    """A mongodb session information blueprint"""
    def __init__(self, initial=None, sid=None):
        sessions.CallbackDict.__init__(self, initial)
        self.sid = sid
        self.modified = False

class MongoSessionInterface(sessions.SessionInterface):
    """Session interface implementation for managing flask sessions on mongodb"""
    def __init__(self, host=None, port=None,
                 db=None, collection='sessions'):
        host = host if host else helpers.db_host
        port = port if port else helpers.db_port
        db = db if db else helpers.db_name
        client = helpers.get_db_instance(host, port)
        self.store = client[db][collection]

    def open_session(self, app, request):
        sid = request.cookies.get(app.session_cookie_name)
        if sid:
            stored_session = self.store.find_one({'sid': sid})
            if stored_session:
                if stored_session.get('expiration') > datetime.datetime.utcnow():
                    return MongoSession(initial=stored_session['data'],
                                        sid=stored_session['sid'])
        sid = str(uuid.uuid4())
        return MongoSession(sid=sid)

    def save_session(self, app, session, response):
        domain = self.get_cookie_domain(app)
        if not session:
            response.delete_cookie(app.session_cookie_name, domain=domain)
            return
        if self.get_expiration_time(app, session):
            expiration = self.get_expiration_time(app, session)
        else:
            expiration = datetime.utcnow() + datetime.timedelta(hours=1)
        self.store.update({'sid': session.sid},
                          {'sid': session.sid,
                           'data': session,
                           'expiration': expiration}, True)
        response.set_cookie(app.session_cookie_name, session.sid,
                            expires=self.get_expiration_time(app, session),
                            httponly=True, domain=domain)
        