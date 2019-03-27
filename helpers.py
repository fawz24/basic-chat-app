# -*- coding: utf-8 -*-

import pymongo
import models

mongo_client = None
db = None

def get_db_instance():
    """Creates an instance of the database then returns that instance.
    If the database is already instanciated simply returns the existing instance."""
    global mongo_client
    global db
    
    if mongo_client is None:
        mongo_client = pymongo.MongoClient()
        
    if db is None:
        db = mongo_client.get_database('chat_network_programming')
    
    return db

def user_exists(user_name):
    """Checks if a user exists."""
    db = get_db_instance()
    
    user = db.users.find_one({"name": user_name})
    if user:
        return True
    return False

def get_user(user_name):
    """Retrieves informations about a particular user"""
    db = get_db_instance()
    
    user = db.users.find_one({'name': user_name})
    if user:
        return models.User(user['name'], user['password'])
    return None
