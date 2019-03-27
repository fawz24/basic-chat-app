# -*- coding: utf-8 -*-

import pymongo

mongo_client = None
db = None

def get_db_instance():
    global mongo_client
    global db
    
    if mongo_client is None:
        mongo_client = pymongo.MongoClient()
        
    if db is None:
        db = mongo_client.get_database('chat_network_programming')
    
    return db

def user_exists(user_name):
    db = get_db_instance()
    
    user = db.users.find_one({"name": user_name})
    if user:
        return True
    return False

