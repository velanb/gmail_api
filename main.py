import json
from gmailModule.gmail_repositories import GmailRepo
from gmailModule.gmail_services import GmailAPI
from ruleFilter import RuleFilter
from datetime import date, timedelta, datetime
from utils import QueryUtils


def main():
    db_config = None
    SCOPES = None
    try:
        with open('config.json') as config:
            config = json.load(config)
            db_config = config['db_config']
            SCOPES = config.get('gmail_scopes')
        gmail_api = GmailAPI(SCOPES)
        gmail_repo = GmailRepo('gmail_api_v1', 'gmail_table_v1', db_config)
        actions = RuleFilter(gmail_api, gmail_repo).apply_rule()
        print("\n")
        print("Result >>>>>", actions)
        return actions
    except FileNotFoundError as err:
        print("Error>>> ", err)


main()
