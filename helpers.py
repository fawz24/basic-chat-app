# -*- coding: utf-8 -*-

import pymongo
import models

mongo_client = None
db = None
db_name = 'chat_network_programming'
db_host = 'localhost'
db_port = 27017

#DB functions
def get_db_instance(host=db_host, port=db_port):
    """Creates an instance of the database then returns that instance.
    If the database is already instanciated simply returns the existing instance."""
    global mongo_client
    global db
    global db_name
    
    if mongo_client is None:
        mongo_client = pymongo.MongoClient(host=host, port=port)
        
    if db is None:
        db = mongo_client.get_database(db_name)
    
    return db

#User functions
def user_exists(nick_name):
    """Checks if a user exists.
    Internally calls get_user function."""
    return get_user(nick_name) is not None

def user_document_2_user_instance(user):
    """Maps a mongodb user document to a User instance"""
    return models.User(user['nick_name'],
                       user['password'],
                       groups=user['groups'])

def user_instance_2_user_document(user):
    """Maps a User instance to a mongodb user document"""
    return {'nick_name': user.nick_name,
            'password': user.password,
            'groups': user.groups}

def get_user(nick_name):
    """Retrieves informations about a particular user"""
    db = get_db_instance()
    
    user = db.users.find_one({'nick_name': nick_name})
    if user:
        return user_document_2_user_instance(user)
    return None

def get_users():
    """Retrieves all registered users"""
    users = []
    
    db = get_db_instance()
    
    _users = db.users.find()
    for u in _users:
        users.append(user_document_2_user_instance(u))
    return users

def save_user(user):
    """Saves a new user into the database."""
    db = get_db_instance()
    
    if isinstance(user, models.User):
        db.users.insert_one(user_instance_2_user_document(user))
        return user

#Group functions
def group_exists(name):
    """Checks if a group exists.
    Internally calls get_group function."""
    return get_group(name) is not None

def group_document_2_group_instance(group):
    """Maps a mongodb group document into a Group instance"""
    return models.Group(group['name'],
                        group['creator'],
                        participants=group['participants'],
                        date=group['date'],
                        reference=group['reference'])

def group_instance_2_group_document(group):
    """Maps a Group instance into a mongodb group document"""
    return {'name': group.name,
            'creator': group.creator,
            'participants': group.participants,
            'date': group.date,
            'reference': group.reference}

def get_group(name):
    """Retrieves informations about a particular group"""
    db = get_db_instance()
    
    group = db.groups.find_one({'name': name})
    if group:
        return group_document_2_group_instance(group)
    return None

def get_groups():
    """Retrieves all available groups"""
    groups = []
    
    db = get_db_instance()
        
    _groups = db.groups.find()
    for g in _groups:
        groups.append(group_document_2_group_instance(g))
    return groups
        
def save_group(group):
    """Saves a new group into the database"""
    db = get_db_instance()
    
    if isinstance(group, models.Group):
        db.groups.insert_one(group_instance_2_group_document(group))
        for u in group.participants:
            join_group(group.name, u)
    return group

def delete_group(name):
    """Deletes a group.
    Makes sure there is no user in the group."""
    try:
        group = get_group(name)
        if group.reference == 0:
            db.groups.delete_one({'name': group.name})
            db.messages.delete_many({'type': 'group', 'receiver': name})
            return True
        else:
            raise Exception(f'{name} still contains user(s)')
    except Exception as e:
        print(e)
        return False
    

def quit_group(gname, uname):
    """Deletes the link between the user and the group.
    Checks and updates the number of users in the group."""
    user = get_user(uname)
    group = get_group(gname)
    
    try:
        ugroups = set(user.groups)
        gparticipants = set(group.participants)
        
        ugroups.remove(group.name)
        gparticipants.remove(user.nick_name)
        
        user.groups = list(ugroups)
        group.participants = list(gparticipants)
        group.reference = len(gparticipants)
        
        db.users.update_one({'nick_name': user.nick_name}, {"$set": {'groups': user.groups}})
        db.groups.update_one({'name': group.name}, {"$set": {'participants': group.participants, 
                             'reference': group.reference}})
        delete_group(group.name)
        
    except Exception as e:
        print(e)
        
def join_group(gname, uname):
    """Joins a user to a group"""
    user = get_user(uname)
    group = get_group(gname)
    
    try:
        ugroups = set(user.groups)
        gparticipants = set(group.participants)
        
        ugroups.add(group.name)
        gparticipants.add(user.nick_name)
        
        user.groups = list(ugroups)
        group.participants = list(gparticipants)
        group.reference = len(group.participants)
        
        db.users.update_one({'nick_name': user.nick_name}, {"$set": {'groups': user.groups}})
        db.groups.update_one({'name': group.name}, {"$set": {'participants': group.participants, 
                             'reference': group.reference}})
        
    except Exception as e:
        print(e)
        
#Message functions
def message_document_2_message_instance(message):
    """Maps a mongodb message document to a Message instance"""
    try:
        return models.Message(message['receiver'],
                              message['sender'],
                              message['content'],
                              ms_type=message['type'],
                              date=message['date'])
    except:
        return None

def message_instance_2_message_document(message):
    """Maps a Message instance to a mongodb message document"""
    try:
        return {'receiver': message.receiver,
                'sender': message.sender,
                'content': message.content,
                'type': message.type,
                'date': message.date}
    except:
        return None

def get_simple_messages(receiver, sender):
    """Retrieves informations about all messages sent by a particular user to a unique receiver and vice versa"""
    messages = []
    
    db = get_db_instance()
    
    _messages = db.messages.find({'type': 'simple',
                                'receiver': {'$in': [receiver, sender]},
                                'sender': {'$in': [receiver, sender]}}).sort('date', pymongo.ASCENDING)
   
    if _messages:
        for m in _messages:
            messages.append(message_document_2_message_instance(m))
    return messages

def get_group_messages(receiver):
    """Retrieves informations about all messages sent in a group"""
    messages = []
    
    db = get_db_instance()
    
    _messages = db.messages.find({'type': 'group',
                                'receiver': receiver}).sort('date', pymongo.ASCENDING)
   
    if _messages:
        for m in _messages:
            messages.append(message_document_2_message_instance(m))
    return messages

def get_broadcast_messages():
    """Retrieves informations about all messages sent to all users"""
    messages = []
    
    db = get_db_instance()
    
    _messages = db.messages.find({'type': 'broadcast'}).sort('date', pymongo.ASCENDING)
   
    if _messages:
        for m in _messages:
            messages.append(message_document_2_message_instance(m))
    return messages

def save_message(message):
    """Saves a new message into the database."""
    db = get_db_instance()
    
    db.messages.insert_one(message_instance_2_message_document(message))
    return message