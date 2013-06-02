from flask.ext.wtf import Form, TextField, BooleanField, FileField
from flask.ext.wtf import Required


class LoginForm(Form):
    username = TextField('username' , validators = [Required()])
    #remember_me = BooleanField('remember_me' , default = False)
    password = TextField('password' , validators = [Required()])

    photo = FileField("Your photo")


class PhotoUpload(Form):

	photoName = TextField('photoName' , validators = [Required()])
	photo = FileField("New photo")


class CreateProject(Form):

	projectName = TextField('projectName' , validators = [Required()])
	description = TextField('description')
