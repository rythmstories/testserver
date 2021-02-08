from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import createtoken, getalltoken, tokenpool, assigntoken, getuserdetails

urlpatterns = [

    url(r'token/', createtoken, name="test"),				# create token (post), delete all token (put), delete specific token (put)
    url(r'all/', getalltoken, name="test"),					# (post) token, to check details / live link for any token / delete the token if it is not updated in 5 min
    url(r'pool/', tokenpool, name="test"),					# to see pool of tokens
    url(r'assign/', assigntoken, name="test"),				# to see free token (GET), assign free token (post) and check whether token exist for same credential
    														# to unblock a token (PUT)

    url(r'user/', getuserdetails, name="test"),				# give all users (get), to get user details (post), delete a user(put) 

]

