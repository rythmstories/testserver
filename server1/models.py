from django.db import models

class Tokendetails(models.Model):
	token = models.CharField(max_length = 200)				# get token value
	statestatus = models.CharField(max_length = 50)			# status of state ie whether its free or blocked
	lasttime = models.DateTimeField()						# last time this token was made live 
	livestatus = models.CharField(max_length = 50)			# status whether it is live or dead
	userpk = models.CharField(max_length = 50)				# user detail, pk of user if it is attached ie token is blocked


class Userdetails(models.Model):
	username = models.CharField(max_length = 200)
	password = models.CharField(max_length = 200)
	tokenid = models.ForeignKey(Tokendetails, on_delete = models.CASCADE)

