from rest_framework import serializers

from .models import Tokendetails, Userdetails 



class TokendetailsSerializer(serializers.ModelSerializer):
	class Meta:
		model = Tokendetails
		field = '__all__'


class UserdetailsSerializer(serializers.ModelSerializer):
	class Meta:
		model = Userdetails
		field = '__all__'

		