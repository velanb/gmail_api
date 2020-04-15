import json
from errorhandler import UtilError
from datetime import datetime, date, timedelta


class AppUtils:
    @staticmethod
    def readJSONFile(filename):
        with open(filename) as this_file:
            return json.load(this_file)


class ActionUtils:
    @staticmethod
    def CreateMsgLabels(remove_label_id_list, add_label_id_list):
        return {'removeLabelIds': remove_label_id_list, 'addLabelIds': add_label_id_list}


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
            "does_not_contain": "does_not_contain",
            "equals": "equals",
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
                predicate = predicate_switcher.get(condition['predicate'])
                if ctr > 0:
                    q3.append(field)
                    q3.append(predicate)
                    q3.append("'%{}%'".format(condition['value']))
                    if ctr - 1 > 0:
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
