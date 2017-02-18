"""Class to store and retrieve data from DB.
"""

import couchdb
import configparser
import json
from uuid import uuid4
from datetime import datetime


class DBCache(object):
    DB_NAME = "bitcoin-model"

    @staticmethod
    def datetime_string(datetime):
        if type(datetime) is datetime:
            return datetime.date().isoformat()
        elif type(datetime) is str:
            return datetime
        else:
            raise TypeError("Object provided to DBCache.datetime_string() is not datetime.")

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read("config.ini")
        url = "http://{}:{}".format(self.config['DB']['hostname'], 
                                    self.config['DB']['port'])
        self.db = couchdb.Server(url)[self.DB_NAME]
        
    def save_doc(self, doc):
        doc_id = uuid4()
        self.db[doc_id] = doc
        
    def save_doc_list(self, list):
        for doc in list:
            doc.store(self.db)
            
    def get_view(self, viewname):
        return self.db.view(viewname)


