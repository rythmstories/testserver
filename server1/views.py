from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import TokendetailsSerializer, UserdetailsSerializer
from .models import Tokendetails, Userdetails 
import datetime
import secrets
from django.utils.timezone import utc
from django.http import Http404
import random


def deletetokenuser(tokenid_to_delete):
	check = Tokendetails.objects.filter(id = tokenid_to_delete).values()
	if check:
		Tokendetails.objects.filter(id = tokenid_to_delete).delete()
		Userdetails.objects.filter(tokenid_id = tokenid_to_delete).delete()
	else:
		print("no corresponding token exist")
	pass


def livethetoken():								# func to live the tokens (both types)
	now = datetime.datetime.now()
	freetoken = Tokendetails.objects.filter(statestatus = 'free').values()
	if freetoken:
		for i in freetoken:
			freetokenid = i['id']
			diff = now.replace(tzinfo=None) - i['lasttime'].replace(tzinfo=None)
			diff_sec = diff.seconds
			if diff_sec <= 300:
				Tokendetails.objects.filter(id = freetokenid).filter(statestatus = 'free').update(lasttime = now)
			elif diff_sec > 300:
				deletetokenuser(freetokenid)

	blockedtoken = Tokendetails.objects.filter(statestatus = 'blocked').values()
	if blockedtoken:
		for i in blockedtoken:
			blockedtokenid = i['id']
			diff = now.replace(tzinfo=None) - i['lasttime'].replace(tzinfo=None)
			diff_sec = diff.seconds

			if diff_sec <= 60:
				Tokendetails.objects.filter(id = blockedtokenid).filter(statestatus = 'blocked').update(lasttime = now)		

			elif diff_sec > 60:					# here we delete user and unblock the token
				Userdetails.objects.filter(tokenid_id = blockedtokenid).delete()			# deleting the user
				Tokendetails.objects.filter(id = blockedtokenid).filter(statestatus = 'blocked').update(statestatus = 'free')
				Tokendetails.objects.filter(id = blockedtokenid).filter(statestatus = 'blocked').update(lasttime = now)
				Tokendetails.objects.filter(id = blockedtokenid).filter(statestatus = 'blocked').update(userpk = "0")
	pass

		# {"name" : "gaurav", "password" : "123"}
		# {"name" : "manav", "password" : "123"}
		# {"name" : "sonia", "password" : "123"}
		# {"name" : "mayur", "password" : "123"}


@api_view(['GET', 'POST', 'PUT'])
def createtoken(request):										# func to create token
	if request.method == 'GET':
		livethetoken()
		return Response("Click POST Button to create 'TOKEN'")

	elif request.method == 'POST':
		livethetoken()
		tkn = secrets.token_hex(20)
		now = datetime.datetime.now()
		Tokendetails.objects.create(
			token = str(tkn),
			statestatus = 'free',
			lasttime = now,
			livestatus = 'live',
			userpk = str(0)
			)
		data = Tokendetails.objects.filter(token = tkn).values()
		return Response(data)

	elif request.method == 'PUT':						# delete token table data ie truncate table for testing is request.data kept clear
		if request.data:								# delete specific token with put request {"token" : token_value}
			livethetoken()
			token_to_delete = request.data['token']
			token_to_delete_details = Tokendetails.objects.filter(token = token_to_delete).values()
			if token_to_delete_details:
				Userdetails.objects.filter(tokenid_id = token_to_delete_details[0]['id']).delete()
				Tokendetails.objects.filter(token = token_to_delete).delete()
				return Response({'note' : 'Token deleted'})
			else:
				return Response({'note' : 'No such token exist.'})
		else:
			Tokendetails.objects.all().delete()	
			Userdetails.objects.all().delete()			
			data = Tokendetails.objects.values()
			if data:
				return Response({'note' : 'All tokens should be deleted but some present'})
			else:
				return Response({'note' : 'All tokens deleted.'})

# Json for PUT request
# {"token": "04d159ecf3ee7cc69f92fec8f2218efdccc9e8ad"}		
# {"token": "28f19a493ccaa8e93b727b3e7ab68e412ff9fd79"}	


@api_view(['GET', 'POST'])
def getalltoken(request):							# func to live the token
	if request.method == 'GET':
		livethetoken()
		data = Tokendetails.objects.values("id", "token", "lasttime", "statestatus")
		if data:
			new = {'token' : data, 'note' : 'To get token information in detail, please click POST button.'}
			return Response(new)
		else:
			return Response({'note' : 'No token is available. Please create token to fetch information.'})
			
	elif request.method == 'POST':					# this will give individual detail of a token and will update time ie live - state
		if 'token' in  request.data:
			token_value = request.data['token']
			token_data = Tokendetails.objects.filter(token = token_value).values("lasttime")
			if token_data :
				now = datetime.datetime.now()
				diff = now.replace(tzinfo=None) - token_data[0]['lasttime'].replace(tzinfo=None)
				diff_sec = diff.seconds
				if diff_sec <= 300 :
					Tokendetails.objects.filter(token = token_value).update(lasttime = now)			# update timing if found within 5 mins 
					token_data = Tokendetails.objects.filter(token = token_value).values()			# updated values
					return Response(token_data)
				else:
					Tokendetails.objects.filter(token = token_value).delete()
					return Response("Since is token was not live for more than 5 min, it si deleted.")
			else:
				return Response("This token doesn't exist.")
		else:
			return Response({'note' : 'Please enter token data.'})

# Json for POST request
# {"token": "04d159ecf3ee7cc69f92fec8f2218efdccc9e8ad"}		
# {"token": "28f19a493ccaa8e93b727b3e7ab68e412ff9fd79"}	


@api_view(['GET'])
def tokenpool(request):								# func to see token pool ie all tokens whether free or blocked

	if request.method == 'GET':
		livethetoken()
		data = Tokendetails.objects.values("id", "token", "lasttime", "statestatus")
		if data:
			return Response(data)
		else:
			return Response({'note' : 'No token is available. Please create token to fetch information.'})



@api_view(['GET', 'POST', 'PUT'])
def assigntoken(request):
	if request.method == 'GET':						# To see only free tokens
		livethetoken()
		data = Tokendetails.objects.filter(statestatus = 'free').values("id", "token", "lasttime", "statestatus")
		if data:
			return Response(data)
		else:
			return Response({'note' : 'No token is available. Please create token to fetch information.'})


	elif request.method == 'POST':					# use for assigning free token to a user
		livethetoken()
		try:
			username = request.data['name']
			userpassword = request.data['password']
		except:
			return Response({'note' : 'Please enter correct username & password.'})
		chechtoken = Userdetails.objects.filter(username = username).filter(password = userpassword).values()		# credentials of user, if already exist
		if chechtoken:								# if user already exist
			dict1 = {}
			now = datetime.datetime.now()
			Tokendetails.objects.filter(id = chechtoken[0]['tokenid_id']).update(lasttime = now)		# this is done to update the token timing ie live-state endpoint for token is hit
			chk = Tokendetails.objects.filter(id = chechtoken[0]['tokenid_id']).values()
			dict1['user'] = chechtoken
			dict1['note'] = "This User credentials already exist."
			return Response(dict1)
		else:
			data = Tokendetails.objects.filter(statestatus = 'free').values("id")
			freetokenlist = []
			if data:
				for i in data:
					freetokenlist.append(i['id'])
				tokenassigned = int(random.choice(freetokenlist))
				token_instance = Tokendetails.objects.filter(id = tokenassigned)
				Userdetails.objects.create(
					username = username,
					password = userpassword,
					tokenid = token_instance[0]
					)
				new_user = Userdetails.objects.filter(tokenid = tokenassigned).values()
				now = datetime.datetime.now()
				Tokendetails.objects.filter(id = tokenassigned).update(lasttime = now)
				Tokendetails.objects.filter(id = tokenassigned).update(statestatus = 'blocked')
				Tokendetails.objects.filter(id = tokenassigned).update(userpk = str(new_user[0]['id']))
				updated_token = Tokendetails.objects.filter(id = tokenassigned).values()
				return Response(new_user)
			else:
				raise Http404()


		# Json for POST request

		# {"name" : "gaurav", "password" : "123"}
		# {"name" : "manav", "password" : "123"}
		# {"name" : "sonia", "password" : "123"}
		# {"name" : "mayur", "password" : "123"}

	elif request.method == 'PUT':					# used for unblocking a token
		livethetoken()
		try:
			username = request.data['name']
			userpassword = request.data['password']
		except:
			return Response({'note' : 'Please enter correct username & password.'})
		chechtoken = Userdetails.objects.filter(username = username).filter(password = userpassword).values()		# credentials of user
		if chechtoken:			# if user exist
			dict1 = {}
			now = datetime.datetime.now()
			Tokendetails.objects.filter(id = chechtoken[0]['tokenid_id']).update(lasttime = now)
			Tokendetails.objects.filter(id = chechtoken[0]['tokenid_id']).update(statestatus = 'free')
			Tokendetails.objects.filter(id = chechtoken[0]['tokenid_id']).update(livestatus = 'live')
			chk = Tokendetails.objects.filter(id = chechtoken[0]['tokenid_id']).values()
			Userdetails.objects.filter(username = username).filter(password = userpassword).delete()
			dict1['user'] = chechtoken
			dict1['note'] = "This user deleted. Allotted token is now free/unblocked."
			dict2 = {}
			dict2['token'] = chk
			dict2['note'] = "This token is now unblocked, free to use."
			main_dict = {}
			main_dict['user'] = dict1
			main_dict['token'] = dict2
			return Response(main_dict)
		else:
			return Response({'note' : 'There is no such user in database.'})

		# Json for PUT request

		# {"name" : "gaurav", "password" : "123"}
		# {"name" : "manav", "password" : "123"}
		# {"name" : "sonia", "password" : "123"}
		# {"name" : "mayur", "password" : "123"}


@api_view(['GET', 'POST', 'PUT'])
def getuserdetails(request):
	if request.method == 'GET':						# to get details of all users
		livethetoken()
		data = Userdetails.objects.values()
		if data:
			return Response(data)
		else:
			return Response({'note' : 'No user created.'})

	elif request.method == 'POST':					# to get detail of a specific user
		livethetoken()
		try:
			username = request.data['name']
			userpassword = request.data['password']
		except:
			return Response({'note' : 'Please enter correct username & password.'})
		userdata = Userdetails.objects.filter(username = username).filter(password = userpassword).values()

		if userdata:
			return Response(userdata)
		else:
			return Response({'note' : 'No such user exist in database.'})

		# Json for POST request
		# {"name" : "gaurav", "password" : "123"}
		# {"name" : "manav", "password" : "123"}
		# {"name" : "sonia", "password" : "123"}
		# {"name" : "mayur", "password" : "123"}

	elif request.method == 'PUT':					# request for deleting specific user
		livethetoken()
		try:
			username = request.data['name']
			userpassword = request.data['password']
		except:
			return Response({'note' : 'Please enter correct username & password.'})
		userdata = Userdetails.objects.filter(username = username).filter(password = userpassword).values()
		if userdata:
			user_data = Userdetails.objects.filter(username = username).filter(password = userpassword).values()
			dict1 = {}
			dict1['note'] = "User is delete and corresponding token is now free."
			token_to_free = user_data[0]['tokenid_id']
			Userdetails.objects.filter(username = username).filter(password = userpassword).delete()
			Tokendetails.objects.filter(id = token_to_free).update(statestatus = 'free')
			Tokendetails.objects.filter(id = token_to_free).update(userpk = '0')
			tokendata = Tokendetails.objects.filter(id = token_to_free).values()
			dict1['token'] = tokendata
			return Response(dict1)
		else:
			return Response({'note' : 'No such user exist in database.'})


		# Json for PUT request
		# {"name" : "gaurav", "password" : "123"}
		# {"name" : "manav", "password" : "123"}
		# {"name" : "sonia", "password" : "123"}
		# {"name" : "mayur", "password" : "123"}



