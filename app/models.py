from app import db

class Photo(db.EmbeddedDocument):
	"""docstring for Photo"""
	photoKey = db.StringField(max_length=255, required = True , unique = True)
	name = db.StringField(max_length=255, required = False)
	placeNumber = db.IntField(min_value = 0, required = True)

class PhotoProject(db.Document):

	projectKey = db.StringField(max_length = 255, required = True, unique = True)
	name = db.StringField(required = True)
	description = db.StringField(required = False)
	photos = db.ListField(db.EmbeddedDocumentField(Photo))
	published = db.BooleanField(default = False) 
	placeNumber = db.IntField(min_value = 0, required = True)
 	
class User(db.Document):

	username = db.StringField(required = True, unique = True)
	password = db.StringField(required= True)
	email = db.EmailField()

	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return unicode(self.username)