# -*- coding: utf-8 -*-

import pymongo
import models

mongo_client = None
db = None
db_name = 'chat_network_programming'
db_host = 'localhost'
db_port = 27017

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
        return models.User(user['name'], user['password'])
    return None

def save_user(user):
    """Saves a new user into the database."""
    db = get_db_instance()
    
    db.users.insert_one({'name': user.nick_name, 'password': user.password})
    return user

#Group functions
def group_exists(name):
    """Checks if a group exists"""
    db = get_db_instance()
    
    group = db.groups.find_one({'name': name})
    return group is not None

def get_group(name):
    """Retrieves informations about a particular group"""
    db = get_db_instance()
    
    group = db.groups.find_one({'name': name})
    if group:
        return models.Group(group['name'], group['creator'], 
                            participants=group['participants'], date=group['date'])
    return None

def save_group(group):
    """Saves a new group into the database"""
    db = get_db_instance()
    
    db.groups.insert_one({'name': group.name, 'creator': group.creator,
                          'participants': group.participants, 'date': group.date})
    return group