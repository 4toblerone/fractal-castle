import boto
from app import app2


def getbucket():
	s3 = boto.connect_s3(aws_access_key_id=app2.config['AWS_ACCESS_KEY_ID'],
					 	aws_secret_access_key=app2.config['AWS_SECRET_ACCESS_KEY'],
					  	debug = 2)
	bucket = s3.get_bucket("fractalcastle")
	return bucket