from app import db
#from flask.ext.sqlalchemy import sqlalchemy



class Photo(db.Model):
	"""docstring for Photo"""
	
	__tablename__ = 'photo'
	#photoid = db.Column('photoid' , db.Integer, primary_key = True )
	photokey = db.Column('photokey' , db.String(35) , primary_key = True)
	projectkey = db.Column('projectkey', db.String , db.ForeignKey('photoproject.projectkey'))
	name = db.Column('name' , db.String(35))
	placenumber = db.Column('placenumber' , db.Integer)
	photourl = db.Column('photourl', db.String)

class PhotoProject(db.Model):

	__tablename__= 'photoproject'
	#projectid = db.Column('projectid',db.Integer, primary_key = True)
	projectkey = db.Column('projectkey',db.String(35), primary_key = True)
	name = db.Column('name',db.String(35))
	description = db.Column('description',db.String(35))
	published = db.Column('published',db.Boolean) 
	placenumber = db.Column('placenumber',db.Integer)
	photos = db.relationship('Photo' , lazy='dynamic')


 	
class User(db.Model):	

	__tablename__= 'user'
	userid = db.Column('userid' , db.Integer,primary_key=True, unique = True)
	username = db.Column('username' , db.String(35), unique = True, primary_key=True)
	password = db.Column('password' , db.String(35))
	email = db.Column('email', db.String(50), unique = True)

	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return unicode(self.username)