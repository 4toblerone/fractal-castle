from flask import Flask
from flask.ext.login import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#app = Flask(__name__)
app2 = Flask(__name__)
app2.config.from_envvar('FRACTALCASTLE_CONFIG')
app2.debug=True
engine = create_engine('mysql+mysqldb://root:admin@localhost/fractalc_db')
Session = sessionmaker(bind=engine)
Base = declarative_base()
#app.config.from_object('config')
#app.config.from_envvar('FRACTALCASTLE_CONFIG')
# db = Session()
# db = SQLAlchemy(app2)
lm = LoginManager()
lm.setup_app(app2)
lm.login_view = 'login'

if __name__ == '__main__':
	app2.run(debug=True)
	
from app import views

