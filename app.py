from flask import Flask
from main import emails

app = Flask(__name__)


@app.route('/')
def getFile():
    email_data = emails
    return {"email_data": email_data}


app.run(debug=True)
