from db import DB
from gmailModule.error_handlers import GmailRepoError
import json

# This class has methods which handles connecting to the db and performing CRUD operations
# This class takes in three parameters to initalize
# @param - db_name - type string - Name of the datavase
# @param - table_name - type string - Name of the table_name
# @param - conn_dict - type dict - The connection Dict withe the db configuration
# This class inherts from the DB class which has all the connection config for the database


class GmailRepo(DB):
    def __init__(self, db_name, table_name, conn_dict):
        super().__init__(db_name, conn_dict)
        self.table_name = table_name
        self.create_table(table_name)

# This method is used to add emails to the database.
# @param - email_dict - type dict - The email dictionary

    def add_emails(self, email_dict):
        if ((email_dict is None) or (not email_dict)):
            raise GmailRepoError(
                'The email_dict cannot be None', 'add_emails')
        if(type(email_dict) != dict):
            raise TypeError('The email_dict should be of type DICT')
        add_email = ("INSERT IGNORE INTO gmail_table_v1 "
                     "(email_id, email_subject, email_body, email_label, sender_info, recieved_date,recieved_time ) "
                     "VALUES (%s, %s, %s, %s, %s, %s, %s)")
        email_label_json = json.dumps({"label": email_dict['email_label']})
        email_data = (email_dict['email_id'], email_dict['email_subject'],
                      email_dict['email_body'], email_label_json, email_dict['sender_info'], email_dict['recieved_date'], email_dict['recieved_time'])
        self._DB__use_database()
        self.cursor.execute(add_email, email_data)
        self.db_connection.commit()

# This method is to fetch the emails form db based on the emailid
# @param - email_id - type string - The email id

    def fetch_email(self, email_id):
        if((not email_id) or (email_id is None)):
            raise GmailRepoError(
                'The email_id cannot be empty', 'fetch_email')
        query = "SELECT * FROM gmail_table_v1 WHERE email_id='{}'".format(
            email_id)
        self._DB__use_database()
        self.cursor.execute(query)
        email_list = []
        for data in self.cursor:
            email_list.append(data)
        return email_list
# This method takes in a query and returns a list of emails
# @param - query - type string

    def fetch_emails(self, query):
        if((not query) or (query is None)):
            raise GmailRepoError(
                'The query parameter is required', 'fetch_emails')
        self._DB__use_database()
        self.cursor.execute(query)
        records = self.cursor.fetchall()
        return records
# This method is to update the email label
# @param - emailid - a string
# @param - label - a JSON

    def update_email_label(self, email_id, label_ids):
        add_email = ("UPDATE gmail_table_v1 "
                     "SET 'email_label' = %s"
                     "WHERE email_id = %s")
        values = (label_ids, email_id)
        query = "UPDATE {} SET 'email_label' = '{}' WHERE 'email_id'='{}' ".format(
            self.table_name, label_ids, email_id)
        self.cursor.execute(add_email, values)
        self.db_connection.commit()
        return True

# This method is to create a table
# @param table_name - type string

    def create_table(self, table_name):
        if((not table_name) or (table_name is None)):
            raise GmailRepoError(
                'The table_name parameter  must be specified', 'create_table')
        self._DB__use_database()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS {} (id INT AUTO_INCREMENT PRIMARY KEY, email_id VARCHAR(50) NOT NULL UNIQUE, email_subject TEXT(65535), email_body TEXT(65535), email_label JSON, sender_info TEXT(1000), recieved_date DATE, recieved_time TIME)".format(table_name))
