from flask import Flask
from flask.ext.mongoengine import MongoEngine
from flask.ext.login import LoginManager
import boto
import os

app = Flask(__name__)
app.config.from_object('config')
#app.config.from_envvar('FRACTALCASTLE_CONFIG')
#db = MongoEngine(app)
lm = LoginManager()
lm.setup_app(app)
lm.login_view = 'login'
#s3 = boto.connect_s3(aws_access_key_id=app.config['AWS_ACCESS_KEY_ID'], aws_secret_access_key=app.config['AWS_SECRET_ACCESS_KEY'], debug = 2)
#bucket = s3.get_bucket("fractalcastle")
if __name__ == '__main__':
	app.run(debug=True)
from app import views