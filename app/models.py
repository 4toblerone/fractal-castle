from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
#from app import engine

Base = declarative_base()
#Base.metadata.create_all(engine)


class Photo(Base):
    """docstring for Photo"""

    __tablename__ = 'photo'
    photo_id = Column('photoid', Integer, primary_key=True)
    photokey = Column('photokey', String(35),  nullable=False)
    projectkey = Column('projectkey', String, ForeignKey('photoproject.projectkey'), nullable=False)
    name = Column('name', String(35), nullable=False)
    placenumber = Column('placenumber', Integer, nullable=False)
    photourl = Column('photourl', String, nullable=False)


class PhotoProject(Base):
    __tablename__ = 'photoproject'
    project_id = Column('projectid', Integer, primary_key = True)
    projectkey = Column('projectkey', String(35), primary_key=True)
    name = Column('name', String(35), nullable=False)
    description = Column('description', String(35), nullable=False, default='')
    published = Column('published', Boolean, nullable=False)
    placenumber = Column('placenumber', Integer, nullable=False,)
    photos = relationship('Photo', lazy='dynamic')


class Page(Base):
    __tablename__='page'
    page_id = Column('id', Integer, primary_key=True, unique=True)
    page_num = Column('pagenum', Integer, nullable=False)
    # photos = relationship('Photo', lazy='dynamic')
    containers = relationship('Container', lazy='dynamic')


class Container(Base):
    __tablename__='container'
    container_id = Column('container_id', Integer, primary_key=True)
    container_num = Column('container_num', Integer, nullable=False)
    photokey = Column('photokey', String, ForeignKey('photo'), nullable=False)
    page_id = Column('page_id', Integer, ForeignKey('page'))
    length = Column('length', Integer)
    height = Column('height', Integer)

    photo = relationship('Photo', lazy='dynamic')


class Position(Base):
    __table__='posiTtion'
    position_id = Column('position_id', Integer, primary_key=True)
    coordinate_x = Column('coordinate_x', Integer)
    coordirnate_y = Column('coordinate_y', Integer)
    name = Column('name', String, nullable=True)

class User(Base):
    __tablename__ = 'user'
    user_id = Column('userid', Integer, primary_key=True, unique=True)
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