from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
#from app import engine

Base = declarative_base()
#Base.metadata.create_all(engine)


class Photo(Base):
    """docstring for Photo"""

    __tablename__ = 'photo'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    photokey = Column('photokey', String(35),  nullable=False)
    # projectkey = Column('projectkey', String, ForeignKey('photoproject.projectkey'), nullable=False)
    name = Column('name', String(35), nullable=False)
    placenumber = Column('placenumber', Integer, nullable=False)
    photourl = Column('photourl', String, nullable=False)
    p_project_id = Column('pproject_id', Integer, ForeignKey('photoproject.id'), nullable=False)


class PhotoProject(Base):
    __tablename__ = 'photoproject'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    projectkey = Column('projectkey', String(35), nullable=False)
    name = Column('name', String(35), nullable=False)
    description = Column('description', String(35), nullable=False, default='')
    published = Column('published', Boolean, nullable=False)
    placenumber = Column('placenumber', Integer, nullable=False,)
    photos = relationship('Photo', lazy='dynamic')


class Page(Base):
    __tablename__ = 'page'
    id = Column('id', Integer, primary_key=True, unique=True, autoincrement=True)
    page_num = Column('pagenum', Integer, nullable=False)
    containers = relationship('Container', backref='page')


class Container(Base):
    __tablename__ = 'container'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    container_num = Column('container_num', Integer, nullable=False)
    name = Column('name', String(55), nullable=False)
    photo_id = Column('photo_id', Integer, ForeignKey('photo.id'), nullable=False)
    page_id = Column('page_id', Integer, ForeignKey('page.id'))
    length = Column('length', Integer)
    height = Column('height', Integer)
    position_id = Column('position_id', Integer, ForeignKey('position.id'))
    position = relationship('Position', backref='container')
    photo = relationship('Photo', backref='container')


class Position(Base):
    __tablename__ = 'position'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    coordinate_x = Column('coordinate_x', Integer)
    coordirnate_y = Column('coordinate_y', Integer)
    name = Column('name', String(55), nullable=True)

class User(Base):
    __tablename__ = 'user'
    id = Column('id', Integer, primary_key=True, unique=True)
    username = Column('username', String(35), unique=True, nullable=False)
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