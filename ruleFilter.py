import json
from utils import AppUtils, QueryUtils, ActionUtils
from gmailModule.gmail_repositories import GmailRepo
from gmailModule.gmail_services import GmailAPI

# This Class has all the methods to apply different filters to the email_subject
# The constructor takes in two parameters
# @param - gmail_api - This is a GmailAPI object
# @param - gmail_repo - This is the GmailRepo objec


class RuleFilter:
    def __init__(self, gmail_api, gmail_repo):
        if type(gmail_api) is not GmailAPI:
            raise TypeError("The gmail_api should be of type GmailAPI")
        if type(gmail_repo) is not GmailRepo:
            raise TypeError("The gmail_repo should be of type GmailRepo")

        self.gmail_api = gmail_api
        self.gmail_repo = gmail_repo
        self.config = None
        self.__get_rule_config()
        self.__init_emails()
# method type - public
# This method is to apply all the rules and fetch the emails

    def apply_rule(self):
        first_conditions_emails = self.__apply_rule_conditions()
        for email in first_conditions_emails:
            self.__apply_rule_actions(
                'me', email["email_id"], email["email_labels"])
        return first_conditions_emails


# Method type private
# this  method is to apply the conditional rules to the email_subject


    def __apply_rule_conditions(self):
        print("Applying Rule Conditions \n")
        rule_config = self.config['rule_config']
        foucs_trait = rule_config['focus_trait']
        conditions = rule_config['conditions']
        query = QueryUtils.build_query(
            foucs_trait, conditions, 'gmail_table_v1')
        res_emails = self.gmail_repo.fetch_emails(query)
        email_list = []
        for email in res_emails:
            label_json = json.loads(email[4])
            email_dict = {
                "email_id": email[1],
                "email_subject": email[2],
                "email_content": email[3],
                "email_from": email[5],
                "email_time": email[6],
                "email_labels": label_json['label']}
            email_list.append(email_dict)
        return email_list

# type private
# this method is to apply different action to the emails from the rule config

    def __apply_rule_actions(self, user_id, email_id, email_labels):
        print("Applying Rule Actions \n")
        rule_config = self.config['rule_config']
        actions = rule_config['actions']

        for action in actions:
            action_name = action['action_name']
            if action_name == 'move_message':
                dest_mailbox = action['action_properties']['to_mailbox']
                remove_label_id_list = []
                if dest_mailbox.upper() not in email_labels:
                    add_label_id_list = email_labels
                    add_label_id_list.append(dest_mailbox.upper())
                    message_labels = ActionUtils.CreateMsgLabels(
                        remove_label_id_list, add_label_id_list)
                    result = self.gmail_api.modify_email(
                        user_id, email_id, message_labels)
                else:
                    print('The label already exists for this email', email_id)

            elif action_name == 'mark_as_read':
                if 'UNREAD' in email_labels:
                    remove_label_id_list = ['UNREAD']
                    add_label_id_list = email_labels
                    add_label_id_list.remove('UNREAD')
                    message_labels = ActionUtils.CreateMsgLabels(
                        remove_label_id_list, add_label_id_list)
                    result = self.gmail_api.modify_email(
                        user_id, email_id, message_labels)
                else:
                    print('The Email is already read', email_id)

            elif action_name == 'mark_as_unread':
                if 'UNREAD' in email_labels:
                    remove_label_id_list = []
                    add_label_id_list = email_labels
                    add_label_id_list.append('UNREAD')
                    message_labels = ActionUtils.CreateMsgLabels(
                        remove_label_id_list, add_label_id_list)
                    result = self.gmail_api.modify_email(
                        user_id, email_id, message_labels)
                else:
                    print('The Email is already unread', email_id)
            else:
                raise Exception("The given action_name is not supported")
        return True

# This is the helper method to fetch the rule file

    def __get_rule_config(self):
        print('Fetching Rule config file \n')
        config = AppUtils.readJSONFile('rules.json')
        self.config = config

# this method initializes all the emails and pushes it into the database

    def __init_emails(self):
        list_email = self.gmail_api.fetch_email_ids('me')
        emaiill = self.gmail_api.fetch_email_content('me', list_email)
        for email in emaiill:
            self.gmail_repo.add_emails(email)
