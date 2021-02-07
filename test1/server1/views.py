# from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import TokendetailsSerializer, UserdetailsSerializer
from .models import Tokendetails, Userdetails 
import datetime
import secrets
from django.utils.timezone import utc
from django.http import Http404
import random


@api_view(['GET', 'POST', 'PUT'])
def checkfunc(request):

	if request.method == 'GET':

		return Response('GET Func works')


	elif request.method == 'POST':

		return Response({'POST' : request.data})


	elif request.method == 'PUT':

		return Response({'PUT' : request.data})


def deletetokenuser(tokenid_to_delete):
	print("tokenid_to_delete", tokenid_to_delete)
	check = Tokendetails.objects.filter(id = tokenid_to_delete).values()
	if check:
		print("token with id tokenid_id delete", Tokendetails.objects.filter(id = tokenid_to_delete).values())
		Tokendetails.objects.filter(id = tokenid_to_delete).delete()

		print("token with id tokenid_id delete", Userdetails.objects.filter(tokenid_id = tokenid_to_delete).values())
		Userdetails.objects.filter(tokenid_id = tokenid_to_delete).delete()
		print("deleted user and token")

	else:
		print("no corresponding token exist")

	pass


def livethetoken():								# func to live the tokens who are free
	print("\n")
	print("live the token func called")
	now = datetime.datetime.now()
	freetoken = Tokendetails.objects.filter(statestatus = 'free').values()
	print("freetoken", freetoken)
	if freetoken:
		for i in freetoken:
			freetokenid = i['id']
			diff = now.replace(tzinfo=None) - i['lasttime'].replace(tzinfo=None)
			diff_sec = diff.seconds
			print("diff_sec", diff_sec)

			if diff_sec <= 300:
				print("update token timing to now")
				Tokendetails.objects.filter(id = freetokenid).filter(statestatus = 'free').update(lasttime = now)
				print(Tokendetails.objects.filter(id = freetokenid).filter(statestatus = 'free').values())

			elif diff_sec > 300:
				print("deleting token")
				deletetokenuser(freetokenid)

	blockedtoken = Tokendetails.objects.filter(statestatus = 'blocked').values()
	if blockedtoken:
		for i in blockedtoken:
			blockedtokenid = i['id']
			print("blockedtokenid", blockedtokenid)
			diff = now.replace(tzinfo=None) - i['lasttime'].replace(tzinfo=None)
			diff_sec = diff.seconds
			print("\n")
			print("diff_sec difference between last request", diff_sec)
			print("\n")

			if diff_sec <= 60:
				print("update token timing to now")
				Tokendetails.objects.filter(id = blockedtokenid).filter(statestatus = 'blocked').update(lasttime = now)
				print(Tokendetails.objects.filter(id = blockedtokenid).filter(statestatus = 'blocked').values())				

			elif diff_sec > 60:					# here we delete user and unblock the token
				print("deleting user as time exceed more than 60 second")
				print("token with id tokenid_id delete", Userdetails.objects.filter(tokenid_id = blockedtokenid).values())

				Userdetails.objects.filter(tokenid_id = blockedtokenid).delete()			# deleting the user

				print("updating token from blocked to free")

				print("token before updation", Tokendetails.objects.filter(id = blockedtokenid).values())

				print(Tokendetails.objects.filter(id = blockedtokenid).filter(statestatus = 'blocked').values())
				Tokendetails.objects.filter(id = blockedtokenid).filter(statestatus = 'blocked').update(statestatus = 'free')
				Tokendetails.objects.filter(id = blockedtokenid).filter(statestatus = 'blocked').update(lasttime = now)
				Tokendetails.objects.filter(id = blockedtokenid).filter(statestatus = 'blocked').update(userpk = "0")
				print("token updated")
				print("token after updation", Tokendetails.objects.filter(id = blockedtokenid).values())

	print("\n")
	pass

		# {"name" : "gaurav", "password" : "123"}
		# {"name" : "manav", "password" : "123"}
		# {"name" : "sonia", "password" : "123"}
		# {"name" : "mayur", "password" : "123"}


@api_view(['GET', 'POST', 'PUT'])
def createtoken(request):

	if request.method == 'GET':
		livethetoken()
		return Response("Click POST Button to create 'TOKEN'")


	elif request.method == 'POST':

		print("\n")
		livethetoken()
		tkn = secrets.token_hex(20)
		print("tkn", tkn)
		# print("type", type(tkn))

		now = datetime.datetime.now()
		Tokendetails.objects.create(
			token = str(tkn),
			statestatus = 'free',
			lasttime = now,
			livestatus = 'live',
			userpk = str(0)
			)

		data = Tokendetails.objects.filter(token = tkn).values()
		print("data", data)
		return Response(data)


	elif request.method == 'PUT':						# delet token table data ie truncate table for testing

		if request.data:
			livethetoken()
			print("post the data")
			token_to_delete = request.data['token']
			token_to_delete_details = Tokendetails.objects.filter(token = token_to_delete).values()
			print("token_to_delete_details", token_to_delete_details)

			if token_to_delete_details:
				Userdetails.objects.filter(tokenid_id = token_to_delete_details[0]['id']).delete()
				print("Userdetails.objects.filter(tokenid_id = token_to_delete_details[0]['id'])", Userdetails.objects.filter(tokenid_id = token_to_delete_details[0]['id']).values())

				Tokendetails.objects.filter(token = token_to_delete).delete()
				print("Tokendetails.objects.filter(token = token_to_delete)", Tokendetails.objects.filter(token = token_to_delete).values())

				# livethetoken()
				return Response({'note' : 'Token deleted'})

			else:
				# livethetoken()
				return Response({'note' : 'No such token exist.'})

		else:
			Tokendetails.objects.all().delete()	
			Userdetails.objects.all().delete()			
			data = Tokendetails.objects.values()
			print("data", data)	

			if data:
				print("token present but it should be deleted")
				# livethetoken()
				return Response({'note' : 'All tokens should be deleted but some present'})
			else:
				# livethetoken()
				return Response({'note' : 'All tokens deleted.'})

# {"token": "04d159ecf3ee7cc69f92fec8f2218efdccc9e8ad"}		
# {"token": "28f19a493ccaa8e93b727b3e7ab68e412ff9fd79"}	



@api_view(['GET', 'POST'])
def getalltoken(request):						# func to live the token
	if request.method == 'GET':
		livethetoken()
		data = Tokendetails.objects.values("id", "token", "lasttime", "statestatus")
		print("data", data)
		if data:
			new = {'token' : data, 'note' : 'To get token information in detail, please click POST button.'}
			# livethetoken()
			return Response(new)
		else:
			# livethetoken()
			return Response({'note' : 'No token is available. Please create token to fetch information.'})
			

	elif request.method == 'POST':									# this will give individual detail of a token and will update time ie live - state

		if 'token' in  request.data:
			token_value = request.data['token']
			token_data = Tokendetails.objects.filter(token = token_value).values("lasttime")

			if token_data :
				now = datetime.datetime.now()
				print("now", now)
				print("token_data[0]['lasttime']", token_data[0]['lasttime'])
				# print("type", type(token_data[0]['lasttime']))
				diff = now.replace(tzinfo=None) - token_data[0]['lasttime'].replace(tzinfo=None)
				diff_sec = diff.seconds
				print("diff_sec", diff_sec)
				if diff_sec <= 300 :
					print("time is less than 5 mins.")
					Tokendetails.objects.filter(token = token_value).update(lasttime = now)			# update timing if found within 5 mins 
					token_data = Tokendetails.objects.filter(token = token_value).values()			# updated values
					print("token_data", token_data)
					print("token present and live")
					return Response(token_data)
				else:
					print("time is more than 5 mins ie token is deleted.")
					Tokendetails.objects.filter(token = token_value).delete()
					print("token deleted")
					return Response("Since is token was not live for more than 5 min, it si deleted.")
			else:
				print("token doesn't exist.")
				return Response("This token doesn't exist.")
		else:
			return Response({'note' : 'Please enter token data.'})


# {"token": "04d159ecf3ee7cc69f92fec8f2218efdccc9e8ad"}		
# {"token": "28f19a493ccaa8e93b727b3e7ab68e412ff9fd79"}	




@api_view(['GET'])
def tokenpool(request):

	if request.method == 'GET':
		livethetoken()
		data = Tokendetails.objects.values("id", "token", "lasttime", "statestatus")
		print("data", data)
		if data:
			# livethetoken()
			return Response(data)
		else:
			# livethetoken()
			return Response({'note' : 'No token is available. Please create token to fetch information.'})




@api_view(['GET', 'POST', 'PUT'])
def assigntoken(request):

	if request.method == 'GET':
		livethetoken()
		data = Tokendetails.objects.filter(statestatus = 'free').values("id", "token", "lasttime", "statestatus")
		print("data", data)
		if data:
			# livethetoken()
			return Response(data)
		else:
			# livethetoken()
			return Response({'note' : 'No token is available. Please create token to fetch information.'})


	elif request.method == 'POST':				# use for assigning token to a user
		livethetoken()
		try:
			username = request.data['name']
			userpassword = request.data['password']
		except:
			return Response({'note' : 'Please enter correct username & password.'})
		chechtoken = Userdetails.objects.filter(username = username).filter(password = userpassword).values()		# credentials of user, if already exist

		if chechtoken:			# if user already exist
			dict1 = {}
			now = datetime.datetime.now()
			Tokendetails.objects.filter(id = chechtoken[0]['tokenid_id']).update(lasttime = now)		# this is done to update the token timing ie live-state endpoint for token is hit
			chk = Tokendetails.objects.filter(id = chechtoken[0]['tokenid_id']).values()
			dict1['user'] = chechtoken
			dict1['note'] = "This User credentials already exist."
			# livethetoken()
			return Response(dict1)
		else:
			data = Tokendetails.objects.filter(statestatus = 'free').values("id")
			print("Free token data", data)
			freetokenlist = []
			if data:
				print("Free token exist.")
				for i in data:
					freetokenlist.append(i['id'])
				print("freetokenlist", freetokenlist)
				tokenassigned = int(random.choice(freetokenlist))
				print("tokenassigned", tokenassigned)
				token_instance = Tokendetails.objects.filter(id = tokenassigned)
				Userdetails.objects.create(
					username = username,
					password = userpassword,
					tokenid = token_instance[0]
					)
				new_user = Userdetails.objects.filter(tokenid = tokenassigned).values()
				print("new_user", new_user)
				now = datetime.datetime.now()
				Tokendetails.objects.filter(id = tokenassigned).update(lasttime = now)
				Tokendetails.objects.filter(id = tokenassigned).update(statestatus = 'blocked')
				Tokendetails.objects.filter(id = tokenassigned).update(userpk = str(new_user[0]['id']))
				updated_token = Tokendetails.objects.filter(id = tokenassigned).values()
				print("updated_token", updated_token)
				# livethetoken()
				return Response(new_user)
			else:
				# livethetoken()
				print("No token is free.")
				raise Http404()

		# {"name" : "gaurav", "password" : "123"}
		# {"name" : "manav", "password" : "123"}
		# {"name" : "sonia", "password" : "123"}
		# {"name" : "mayur", "password" : "123"}

	elif request.method == 'PUT':
		livethetoken()
		try:
			username = request.data['name']
			userpassword = request.data['password']
		except:
			return Response({'note' : 'Please enter correct username & password.'})
		chechtoken = Userdetails.objects.filter(username = username).filter(password = userpassword).values()		# credentials of user

		if chechtoken:			# if user exist
			print("chechtoken[0]['tokenid_id']", chechtoken[0]['tokenid_id'])
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
			# livethetoken()
			return Response(main_dict)

		else:
			# livethetoken()
			return Response({'note' : 'There is no such user in database.'})

		# {"name" : "gaurav", "password" : "123"}
		# {"name" : "manav", "password" : "123"}
		# {"name" : "sonia", "password" : "123"}
		# {"name" : "mayur", "password" : "123"}



@api_view(['GET', 'POST', 'PUT'])
def getuserdetails(request):

	if request.method == 'GET':
		livethetoken()
		data = Userdetails.objects.values()
		if data:
			return Response(data)
		else:
			return Response({'note' : 'No user created.'})

	elif request.method == 'POST':
		livethetoken()
		try:
			username = request.data['name']
			userpassword = request.data['password']
		except:
			return Response({'note' : 'Please enter correct username & password.'})
		userdata = Userdetails.objects.filter(username = username).filter(password = userpassword).values()

		if userdata:
			# livethetoken()
			return Response(userdata)
		else:
			# livethetoken()
			return Response({'note' : 'No such user exist in database.'})

		# {"name" : "gaurav", "password" : "123"}
		# {"name" : "manav", "password" : "123"}
		# {"name" : "sonia", "password" : "123"}
		# {"name" : "mayur", "password" : "123"}

	elif request.method == 'PUT':
		livethetoken()
		try:
			username = request.data['name']
			userpassword = request.data['password']
		except:
			return Response({'note' : 'Please enter correct username & password.'})
		userdata = Userdetails.objects.filter(username = username).filter(password = userpassword).values()
		print("userdata to delete", userdata)

		if userdata:
			user_data = Userdetails.objects.filter(username = username).filter(password = userpassword).values()
			print("user_data to delete", user_data)
			dict1 = {}
			# dict1['user'] = user_data
			dict1['note'] = "User is delete and corresponding token is now free."
			print("dict1", dict1)

			print("\n")
			print("user_data", user_data)
			print("type", user_data)
			print("user_data[0]", user_data[0])
			print("\n")

			print("user_data[0]['tokenid_id']", user_data[0]['tokenid_id'])
			token_to_free = user_data[0]['tokenid_id']

			Userdetails.objects.filter(username = username).filter(password = userpassword).delete()

			Tokendetails.objects.filter(id = token_to_free).update(statestatus = 'free')
			Tokendetails.objects.filter(id = token_to_free).update(userpk = '0')
			tokendata = Tokendetails.objects.filter(id = token_to_free).values()
			print("tokendata where token is now free", tokendata)
			dict1['token'] = tokendata
			print("dict1", dict1)
			# livethetoken()
			return Response(dict1)
		else:
			# livethetoken()
			return Response({'note' : 'No such user exist in database.'})


		# {"name" : "gaurav", "password" : "123"}
		# {"name" : "manav", "password" : "123"}
		# {"name" : "sonia", "password" : "123"}
		# {"name" : "mayur", "password" : "123"}



