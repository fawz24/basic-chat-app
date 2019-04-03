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
def user_exists(user_name):
    """Checks if a user exists."""
    db = get_db_instance()
    
    user = db.users.find_one({"name": user_name})
    return user is not None

def get_user(user_name):
    """Retrieves informations about a particular user"""
    db = get_db_instance()
    
    user = db.users.find_one({'name': user_name})
    if user:
        return models.User(user['name'], user['password'], groups=user['groups'])
    return None

def save_user(user):
    """Saves a new user into the database."""
    db = get_db_instance()
    
    db.users.insert_one({'name': user.nick_name, 'password': user.password, 'groups': user.groups})
    return user

#Group functions
def group_exists(name):
    """Checks if a group exists"""
    db = get_db_instance()
    
    group = db.groups.find_one({'name': name})
    return group is not None

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
    groups = set()
    
    db = get_db_instance()
        
    _groups = db.groups.find()
    for g in _groups:
        groups.add(group_document_2_group_instance(g))
    return groups
        
def save_group(group):
    """Saves a new group into the database"""
    db = get_db_instance()
    
    db.groups.insert_one({'name': group.name, 'creator': group.creator,
                          'participants': group.participants, 'date': group.date, 
                          'reference': group.reference})
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
    except Exception:
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
        
        user.groups = ugroups
        group.participants = gparticipants
        group.reference = len(gparticipants)
        
        db.users.update_one({'name': user.nick_name}, {"$set": {'groups': user.groups}})
        db.groups.update_one({'name': group.name}, {"$set": {'participants': group.participants, 
                             'reference': group.reference}})
        
        delete_group(group.name)
        
    except Exception:
        pass
    