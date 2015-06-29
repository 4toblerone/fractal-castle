from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship, backref
# from app import db
# from flask.ext.sqlalchemy import sqlalchemy
from app import Base


class Photo(Base):
    """docstring for Photo"""

    __tablename__ = 'photo'
    # photoid = Column('photoid' , Integer, primary_key = True )
    photokey = Column('photokey', String(35), primary_key=True)
    projectkey = Column('projectkey', String, ForeignKey('photoproject.projectkey'))
    name = Column('name', String(35))
    placenumber = Column('placenumber', Integer)
    photourl = Column('photourl', String)


class PhotoProject(Base):
    __tablename__ = 'photoproject'
    # projectid = db.Column('projectid',db.Integer, primary_key = True)
    projectkey = Column('projectkey', String(35), primary_key=True)
    name = Column('name', String(35))
    description = Column('description', String(35))
    published = Column('published', Boolean)
    placenumber = Column('placenumber', Integer)
    photos = relationship('Photo', lazy='dynamic')


# class Page(Base):
#     id = Column('id', Integer, primary_key=True, unique=True)
#     photos = relationship('Photo', lazy='dynamic')
#

class User(Base):
    __tablename__ = 'user'
    userid = Column('userid', Integer, primary_key=True, unique=True)
    username = Column('username', String(35), unique=True, primary_key=True)
    password = Column('password', String(35))
    email = Column('email', String(50), unique=True)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.username)
