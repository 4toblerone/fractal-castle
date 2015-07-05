from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
#from app import engine

Base = declarative_base()
#Base.metadata.create_all(engine)


class Photo(Base):
    """docstring for Photo"""

    __tablename__ = 'photo'
    # photoid = Column('photoid' , Integer, primary_key = True )
    photokey = Column('photokey', String(35), primary_key=True, nullable=False)
    projectkey = Column('projectkey', String, ForeignKey('photoproject.projectkey'), nullable=False)
    name = Column('name', String(35), nullable=False)
    placenumber = Column('placenumber', Integer, nullable=False)
    photourl = Column('photourl', String, nullable=False)


class PhotoProject(Base):
    __tablename__ = 'photoproject'
    # projectid = db.Column('projectid',db.Integer, primary_key = True)
    projectkey = Column('projectkey', String(35), primary_key=True)
    name = Column('name', String(35), nullable=False)
    description = Column('description', String(35), nullable=False, default='')
    published = Column('published', Boolean, nullable=False)
    placenumber = Column('placenumber', Integer, nullable=False,)
    photos = relationship('Photo', lazy='dynamic')


# class Page(Base):
#     id = Column('id', Integer, primary_key=True, unique=True)
#     photos = relationship('Photo', lazy='dynamic')
#

class User(Base):
    __tablename__ = 'user'
    userid = Column('userid', Integer, primary_key=True, unique=True)
    username = Column('username', String(35), unique=True, primary_key=True, nullable=False)
    password = Column('password', String(35), nullable=False)
    email = Column('email', String(50), unique=True, nullable=False)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.username)