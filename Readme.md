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


## Run Application

The application can be run using the below commands

```
python main.py
```
