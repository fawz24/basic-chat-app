# -*- coding: utf-8 -*-

import datetime

class User:
    """
    User defines a simple user in the chat
    """
    def __init__(self, nick_name, password):
        self.nick_name = nick_name
        self.password = password
        
        
class Message:
    """
    The Message class represents a message sent and received in a chat
    """
    def __init__(self, receiver, sender, content):
        self.receiver = receiver
        self.sender = sender
        self.content = content
        self.date = datetime.datetime.now()

class Group:
    """
    Group is a representation of a chat group
    """
    def __init__(self, name, creator):
        self.name = name
        self.creator = creator
        self.participants = [creator]
        self.date = datetime.datetime.now()