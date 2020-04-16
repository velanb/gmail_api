# Gmail-App 

This is a python stand-alone application which interacts with the gmail-client-api and handles the emails based on different filters
The Gmail auth is done using Oauth using the native gmail client.

### Prerequisites
```
Python version - Python 3.8.2
Database - MySQL 
The app packages can be found in requirements.txt file
```

### Installing

The application uses Gmail's native API to interact with the emails. 
 This is to install the requirements
 ```
    pip install -r requirements.txt
```
To successfully connect with the google servers please login to your gmail and generate the credentials and update the gmail_credentials.json file.

Parameters required -  Client Id, Client Secret and the Project Id. 

You can also replace this file with the credentials.json file downloaded form google API. It requires that the file should be renamed to gmail_credentials.json 


## Configure rules
You can configure the search filters/rules in the rules.json file. 
Below is a sample rule configuration

```
{
  "rule_name": "rule1",         ->> The name of the rule
  "rule_config": {              ->> The configuration
    "focus_trait": "all",       ->> Focus trait
    "conditions": [{            ->> The conditions list.
        "field_name": "from",
        "predicate": "contains",
        "value": "tenmiles"
      },
      {
        "field_name": "from",
        "predicate": "contains",
        "value": "tenmiles"
      },
      {
        "field_name": "subject",
        "predicate": "contains",
        "value": "interview"
      }
    ],
    "actions": [{                             ->> Actions list 
        "action_name": "move_message",
        "action_properties": {
          "to_mailbox": "INBOX"
        }
      },
      {
        "action_name": "mark_as_unread",
        "action_properties": null
      }
    ]
  }
}
```

Below are the available configurations and actions available for

### Focus Trait

```
 "focus_trait": "all"  // The focus trait can be all or any
```
### Condition Dict

```
{
      "field_name": "from",    -> Available Field Names --> from / body / from / to / date
      "predicate": "contains", -> Available Predicates --> contains / does_not_contain / equals / not_equals / greater_than / less_than
      "value": "tenmiles"      -> Any value 
}
```

### Action Dict

```
{
    "action_name": "move_message",  -> Available Action Names - move_message / mark_as_unread / mark_as_read 
    "action_properties": {"to_mailbox": "INBOX"}  -> Destination Labels / null for marking as read or unread
}
```

## Run Application

The application can be run using the below commands

```
python main.py
```
