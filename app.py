#this app.py file initiates flask (a microframework allowing simple URL routing & request handling
#Here, flask's only job is to receive an HTTP request (i.e. user query) and hand it off to the Service Layer
#1 the code below imports Flask into the project/github repo, essentially stating that we will use Flask
from flask import Flask
#2 the code below creates the actual Flask app, BUT not the db, parser, service layer, etc
app = Flask(__name__)
