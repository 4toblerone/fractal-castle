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
s3 = boto.connect_s3(aws_access_key_id=app2.config['AWS_ACCESS_KEY_ID'],
					 aws_secret_access_key=app2.config['AWS_SECRET_ACCESS_KEY'], debug = 2)
bucket = s3.get_bucket("fractalcastle")
if __name__ == '__main__':
	app2.run(debug=True)
	
from fractalcastle.app import views

