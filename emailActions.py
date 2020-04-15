import json
from utils import AppUtils, QueryUtils, ActionUtils
from gmailModule.gmail_repositories import GmailRepo
from gmailModule.gmail_services import GmailAPI


class Actions:
    def __init__(self, gmail_api, gmail_repo):
        self.gmail_api = gmail_api
        self.gmail_repo = gmail_repo
        self.config = None
        self.__get_rule_config()
        self.__init_emails()

    def __apply_rule_conditions(self):
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

    def apply_rule(self):
        first_conditions_emails = self.__apply_rule_conditions()
        for email in first_conditions_emails:
            self.__apply_rule_actions(
                'me', email["email_id"], email["email_labels"])
        return first_conditions_emails
        # self.__init_emails()

    def __apply_rule_actions(self, user_id, email_id, email_labels):
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
        return True

    def __get_rule_config(self):
        config = AppUtils.readJSONFile('rules.json')
        self.config = config

    def __init_emails(self):
        list_email = self.gmail_api.fetch_email_ids('me')
        emaiill = self.gmail_api.fetch_email_content('me', list_email)
        for email in emaiill:
            self.gmail_repo.add_emails(email)
