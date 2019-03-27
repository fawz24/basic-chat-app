# -*- coding: utf-8 -*-

import datetime
import hashlib

class User:
    """User defines a simple user in the chat"""
    def __init__(self, nick_name, password):
        h = hashlib.sha256()
        h.update(password.encode())
        self.nick_name = nick_name
        self.password = h.hexdigest()
        
    def compare(self, user):
        """Compares the nick_name and password fields of the current instance object and another instance object"""
        if self.nick_name != user.nick_name:
            return False
        if self.password != user.password:
            return False
        return True
        
class Message:
    """The Message class represents a message sent and received in a chat"""
    def __init__(self, receiver, sender, content):
        self.receiver = receiver
        self.sender = sender
        self.content = content
        self.date = datetime.datetime.now()

class Group:
    """Group is a representation of a chat group"""
    def __init__(self, name, creator, participants = None):
        self.name = name
        self.creator = creator
        self.participants = participants if participants else [creator]
        self.date = datetime.datetime.now()
        
    def compare(self, group):
        """Compare the name and creator fields of the current instance object to another instance object's same fields"""
        if self.name != group.name:
            return False
        if self.creator != group.creator:
            return False
        return True