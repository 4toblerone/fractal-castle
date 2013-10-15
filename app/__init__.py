from flask import Flask
from flask.ext.login import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy
import boto
import os


#app = Flask(__name__)
app2 = Flask(__name__)
app2.config.from_envvar('FRACTALCASTLE_CONFIG')
app2.debug=True
#app.config.from_object('config')
#app.config.from_envvar('FRACTALCASTLE_CONFIG')
db = SQLAlchemy(app2)
lm = LoginManager()
lm.setup_app(app2)
lm.login_view = 'login'

if __name__ == '__main__':
	app2.run(debug=True)
	
from fractalcastle.app import views

