from flask import Flask
from flask.ext.login import LoginManager
from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# app = Flask(__name__)
app2 = Flask(__name__)
app2.config.from_envvar('FRACTALCASTLE_CONFIG')
app2.debug = True
# create string from config file
DB_STRING = 'mysql+mysqldb://root:admin@localhost/fc_test_3'
engine = create_engine(DB_STRING)
Session = sessionmaker(bind=engine)
# Base = declarative_base()
# Base.metadata.create_all(engine)
# app.config.from_object('config')
# app.config.from_envvar('FRACTALCASTLE_CONFIG')
# db = Session()
# db = SQLAlchemy(app2)
lm = LoginManager()
lm.setup_app(app2)
lm.login_view = 'login'
# from app.db.alembic.env import Base
if __name__ == '__main__':
    app2.run(debug=True)

from app import views
