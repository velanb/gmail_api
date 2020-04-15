import json
from gmailModule.gmail_repositories import GmailRepo
from gmailModule.gmail_services import GmailAPI
from emailActions import Actions
from datetime import date, timedelta, datetime
from utils import QueryUtils


def pre_build():
    db_config = None
    SCOPES = None
    try:
        with open('config.json') as config:
            config = json.load(config)
            db_config = config['db_config']
            SCOPES = config.get('gmail_scopes')
        gmail_api = GmailAPI(SCOPES)
        gmail_repo = GmailRepo('gmail_api_v1', 'gmail_table_v1', db_config)
        actions = Actions(gmail_api, gmail_repo).apply_rule()

    except FileNotFoundError as err:
        print("Error>>> ", err)
