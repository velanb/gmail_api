import json
from errorhandler import UtilError
from datetime import datetime, date, timedelta
# This File contains all the Utility methods that are used across the application

# AppUtil - Consists of global methods used in the applicatio


class AppUtils:
    @staticmethod
    def readJSONFile(filename):
        try:
            with open(filename) as this_file:
                return json.load(this_file)
        except FileNotFoundError as err:
            print("Error>>> ", err)

# Action Util - This contains all the methods to apply rules to emails


class ActionUtils:
    @staticmethod
    def CreateMsgLabels(remove_label_id_list, add_label_id_list):
        if type(remove_label_id_list) is not list or type(add_label_id_list) is not list:
            raise TypeError(
                "Error at CreateMSG Util - the value must be of type list")

        return {'removeLabelIds': remove_label_id_list, 'addLabelIds': add_label_id_list}

# Has the methods for building the query as per the users requirement


class QueryUtils:
    @staticmethod
    def build_query(foucs, conditions, table_name):
        if ((conditions is None) or(not conditions)):
            raise UtilError('The condition must be specified', 'basic_query')

        if((table_name is None) or (not table_name)):
            raise UtilError('The table name must be specified', 'basic_query')

        if(type(conditions) != list):
            raise TypeError('The conditions must be of type list')

        ctr = len(conditions)
        q1 = "SELECT * FROM {} WHERE ".format(table_name)
        q3 = []
        date_metric = []
        query_string = " "
        field_switcher = {
            "subject": "email_subject",
            "body": "email_body",
            "from": "sender_info",
            "to": "sender_info",
            "date": "recieved_date"
        }
        predicate_switcher = {
            "contains": "LIKE",
            "does_not_contain": "NOT LIKE",
            "equals": "=",
            "not_equals": "NOT LIKE",
            "greater_than": ">",
            "less_than": "<"
        }

        focus_switcher = {
            "all": "AND",
            'any': "OR"
        }

        for condition in conditions:
            if condition['field_name'] == 'date':
                date_metric.append(condition)
                ctr = ctr - 1

            else:
                field = field_switcher.get(condition['field_name'])
                if field is None:
                    raise UtilError('Please enter a valid field name in the rule.json file',
                                    "build_query")
                predicate = predicate_switcher.get(condition['predicate'])
                if predicate is None:
                    raise UtilError('Please enter a valid predicate in the rule.json file',
                                    "build_query")
                if ctr > 0:
                    q3.append(field)
                    q3.append(predicate)
                    q3.append("'%{}%'".format(condition['value']))
                    if ctr - 1 > 0:
                        cur_focus = focus_switcher[foucs]
                        if cur_focus is None:
                            raise UtilError(
                                "Please enter a valid focus in the rules.json file ", "build_query")
                        q3.append(focus_switcher[foucs])
                ctr = ctr - 1

        final_query = q1+query_string.join(q3)
        return QueryUtils.date_adv_query(date_metric, final_query)

    @staticmethod
    def date_adv_query(date_cond, old_query):
        if len(date_cond) == 0:
            return old_query+";"
        elif len(date_cond) > 1:
            raise Exception(
                "Its not possible to have more than two date conditions")
        else:
            predicate_switcher = {
                "less_than": "<",
                "greater_than": ">"
            }
            predicate = date_cond[0]['predicate']
            current_date = datetime.now() - \
                timedelta(days=date_cond[0]['value'])

            return old_query + " recieved_date {} '{}'".format(predicate_switcher[predicate], current_date.date()) + ";"
