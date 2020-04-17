import mysql.connector
from errorhandler import DBError


class DB:
    """This is the class with takes care the Database connectuon
@param - db_name - type string - name of the database
@param - connct_dict - type dict - the connection dictionary
"""

    def __init__(self, db_name, conn_dict):
        if((conn_dict is None) or (not conn_dict)):
            raise DBError(
                'The connection dictionary must be specified', 'Error Initializing DB')
        if((db_name is None) or (not db_name)):
            raise DBError('The database name must be specified',
                          'Error Initializing DB')
        if(type(conn_dict) != dict):
            raise TypeError('The connection dictionary must be dict')
        print("Connecting to Database \n")
        self.db_connection = mysql.connector.connect(**conn_dict)
        self.cursor = self.db_connection.cursor()
        self.__db_name = db_name
        self.create_database()

    def create_database(self):
        """The method to create the database
"""
        try:
            self.cursor.execute(
                "CREATE DATABASE IF NOT EXISTS {} DEFAULT CHARACTER SET 'utf8'".format(self.__db_name))
            print("Database Connected \n")
        except mysql.connector.Error as err:
            print("Failed creating database: {}".format(err))

    def __use_database(self):
        """The method to use the specific database
private method
"""
        self.cursor.execute('USE {}'.format(self.__db_name))
