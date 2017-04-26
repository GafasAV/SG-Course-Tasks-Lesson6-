import logging
from mongo_connector import MongoDataStore


__author__ = "Andrew Gafiychuk"


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    logging.debug("[+]Test App MongoDataStore...")

    db = MongoDataStore(db_name="test", table="test")
    record = ("SomeAuthor", "SomeAuthor Title", "http://google2000.com/search", "....Some Data....")

    db.insert_unique(*record)

    logging.debug("[+]Data inserting, try to get back...")
    res_list = db.get_all_data()

    logging.debug("[+]Try to get all docs in collection...")
    for record in res_list:
        print("User: {0}\n"
              "Title: {1}\n"
              "Link: {2}\n"
              "Post: {3}\n"
              .format(*record))

    logging.debug("[+]Try to get all docs by author...")
    res_list = db.get_data_by_author("SomeAuthor")

    for record in res_list:
        print(*record)

    logging.debug("[+]App Done !!!")