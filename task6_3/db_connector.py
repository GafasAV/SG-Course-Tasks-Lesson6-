import psycopg2
import logging


__author__ = "Andrew Gafiychuk"


class DBConnector(object):
    """
    Class for create and connect to data base, for saving
    parsed data from overclockers.ua.
    Used PostgreSQL.
    Create table named overclockers.
    _connect() - create DB connecting use(username, passwd, host, db_name, table_name)
    _create_table() - create overclockers table.
    push_data() - takes 4 params and save it in DB.
    
    """

    def __init__(self, user="postgres", password="12345",
                 host="localhost", db_name="postgres", table="overclockers"):
        """
        Init DB params for connecting.
        
        """
        self.user = user
        self.passwd = password
        self.host = host
        self.db_name = db_name
        self.table = table

        self.conn = None
        self.cursor = None

        self._connect()

    def __del__(self):
        if self.cursor or self.conn:
            self.cursor.close()
            self.conn.close()

    def _connect(self):
        """
        Create DB connecting uses main params.
        return DB cursor as self.cursor
        
        """
        logging.debug("[+]DB Connecting...")

        try:
            self.conn = psycopg2.connect(database=self.db_name,
                                         user=self.user,
                                         password=self.passwd,
                                         host=self.host)

            self.cursor = self.conn.cursor()
            self._create_table()

            logging.debug("[+]DB Connected success !!!")

        except psycopg2.Error as db_err:
            logging.error("[+]DB Connecting problem...\n"
                          "{0}".format(db_err))

    def _create_table(self):
        """
        Create table in self.table.
        Table - overclockers.
        
        """
        try:
            self.cursor.execute(
                "CREATE TABLE IF NOT EXISTS {0}"
                "(id SERIAL PRIMARY KEY,"
                "author VARCHAR (120),"
                "title TEXT ,"
                "link VARCHAR ,"
                "post TEXT);".format(self.table))

            self.conn.commit()

            logging.debug("[+]Table {0} created !!!"
                          .format(self.table))

        except psycopg2.Error as db_err:
            logging.debug("[+]Table creating error...\n"
                          "{0}".format(db_err))

    def push_data(self, author, title, link, post):
        """
        Takes params and save it in DB.
        
        """
        try:
            self.cursor.execute(
                '''INSERT INTO {0} (author, title, link, post)
                 VALUES (%s, %s, %s, %s);'''.format(self.table),
                (author, title, link, post))

            self.conn.commit()

            print("Data saved...")

        except psycopg2.Error as db_err:
            logging.error("[+]Data save error...\n"
                          "[+]DB\Connecting problem..."
                          "{0}".format(db_err))
            raise db_err

    def get_all_data(self):
        """
        Loads data from DB and return it.
        
        """
        try:
            self.cursor.execute("SELECT * FROM {0};"
                                .format(self.table))
            data = self.cursor.fetchall()

            return data

        except psycopg2.Error as db_err:
            logging.debug("[+]Get data error...\n"
                          "{0}".format(db_err))

    def get_data_by_author(self, author):
        """
        Load all post for input author
        
        """
        try:
            self.cursor.execute(
                "SELECT * FROM {0} WHERE author = %s"
                .format(self.table), (author, ))

            data = self.cursor.fetchall()

            return data

        except psycopg2.Error as db_err:
            logging.debug("[+]Get data error...\n"
                          "{0}".format(db_err))


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    logging.debug("[+]App started...")

    db = DBConnector()

    logging.debug("[+]App done !!!")
