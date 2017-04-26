import logging
import pymongo


__author__ = "Andrew Gafiychuk"


class MongoDataStore(object):
    """
    Class for create and connect to data base, for saving
    parsed data from overclockers.ua.
    Used MongoDB.
    Create db and collection named overclockers.
    
    _connect() - create DB connecting use(host, db_name, table_name)
    _create_collection() - create overclockers collection.
                           Set an unique index by <link> row. 
    insert_unique() - takes 4 params and save it in DB. 
                      Check <link> too uniqued.
    get_all_data() - Select ALL docs from collection.
    get_data_by_author() - Selects all documents for one specified author. 
    
    """

    def __init__(self, host="localhost",
                 db_name="overclockers", table="overclockers"):
        """
        Init all params for connecting to MongoDB.

        """
        self.host = host
        self.db_name = db_name
        self.collection_name = table

        self.client = None
        self.db = None
        self.coll = None

        self._connect()

    def __del__(self):
        """
        Check if connecting steel alive and close them if.
        
        """
        if self.client:
            self.client.close()

    def _connect(self):
        """
        Connect to DB.
        
        """
        try:
            self.client = pymongo.MongoClient(host=self.host, port=27017)

            self._create_collection()
        except:
            logging.error("[+]MongoDB connecting problem...")

    def _create_collection(self):
        """
        Create collection for specified DB.
        Set link-row to unique index.
        
        """
        self.db = self.client[self.db_name]
        self.coll = self.db[self.collection_name]

        # Unique record post by hiper-link
        self.coll.create_index([("link", pymongo.ASCENDING)],
                               unique=True)

    def insert_unique(self, author, title, link, post):
        """
        Insert data into collection without duplicate.
        Checked by link.
        
        """
        doc = {"author": author, "title": title,
               "link": link, "post": post}

        try:
            result = self.coll.insert_one(doc)

            print(">>>Data inserting success !!! ID {0}"
                  .format(result.inserted_id))

        except:
            logging.error("[+]Data insert error...\n")

    def get_all_data(self):
        """
        Loads ALL docs from coll. and return it.
 
        """
        try:
            cursor = self.coll.find({})
            result = []

            for record in cursor:
                result.append((*record.values(),)[1:5])

            return result
        except:
            logging.error("[+]Get data error...\n")

    def get_data_by_author(self, author):
        """
        Load all docs for specified author.

        """
        try:
            cursor = self.coll.find({"author": author})
            result = []

            for record in cursor:
                result.append((*record.values(),)[1:5])

            return result
        except:
            logging.error("[+]Get data error...\n")
