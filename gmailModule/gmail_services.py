from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from datetime import datetime
from gmailModule.error_handlers import GmailAPIError


class GmailAPI:
    """The GmailAPI class takes care of all the methods that handle the gmail services
The Constructor takes in one param
@param - scopes - type list - an array of scopes
"""

    def __init__(self, scopes):
        self.SCOPES = scopes
        self.service = self.__create_service()

    def __create_service(self):
        """This method is to create a gmail service instance
"""
        print("Setting Up GMail service..... \n")
        creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'gmail_credentials.json', self.SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        service = build('gmail', 'v1', credentials=creds)
        return service

    def fetch_email_ids(self, user_id):
        """This takes in the userid and get all the emailids
@param - userId - type string"""
        if ((user_id is None)or (not user_id)):
            raise GmailAPIError(
                'The User ID cannot be null', 'fetch_email_ids')
        results = self.service.users().messages().list(
            userId='{}'.format(user_id)).execute()
        labels = results.get('messages')
        item_list = []
        if not labels:
            print('No Emails found')
        else:
            for id in labels:
                item_list.append(id['id'])
            return item_list

    def fetch_email_content(self, user_id, id_list):
        """
This is to fetch all the email contents from the gmail service.
@param - user_id - type string
@param - idlist - type list"""
        print("Fetching Emails ...\n")
        if ((user_id is None)or (not user_id)):
            raise GmailAPIError(
                'The User ID cannot be null', 'fetch_email_ids')
        if(id_list is None):
            raise GmailAPIError(
                'The ID list cannot be null', 'fetch_email_content')
        if(type(id_list) != list):
            raise TypeError(
                'The id_list in fetch_email_content must be of type LIST')
        email_list = []

        for id in id_list:
            result = self.service.users().messages().get(
                userId='{}'.format(user_id), id='{}'.format(id)).execute()
            email_dict = {}
            email_dict['email_id'] = result['id']
            email_dict['email_body'] = result['snippet']
            email_dict['email_label'] = result['labelIds']
            header_list = result['payload']['headers']
            for header in header_list:
                self.__email_dict_generator(header, email_list, email_dict)
            email_list.append(email_dict)
        return email_list

    def modify_email(self,  user_id, email_id, message_labels):
        result = self.service.users().messages().modify(userId=user_id, id=email_id,
                                                        body=message_labels).execute()
        return result

    def __email_dict_generator(self, header, email_list, email_dict):
        """This is a helper method to segregate the emails objects
"""
        if(header['name'] == 'From'):
            email_dict['sender_info'] = header['value']
        elif(header['name'] == 'Date'):
            date_str = header['value']
            rec_day = date_str[0:3]
            rec_date = date_str[5:16]
            rec_time = date_str[16:25]
            rec_zone = date_str[25:31]
            rec_zone_str = date_str[31:37]
            date_obj = datetime.strptime(
                rec_date, '%d %b %Y')
            email_dict['recieved_on_day'] = rec_day
            email_dict['recieved_date'] = date_obj
            email_dict['recieved_time'] = rec_time
        elif(header['name'] == 'Subject'):
            email_dict['email_subject'] = header['value']
            email_list.append(email_dict)
