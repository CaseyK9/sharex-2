from rest_framework import serializers
from rest_framework.serializers import raise_errors_on_nested_writes, model_meta

from .models import Account
from request.models import Request
from car.models import Car
from travel.models import Travel
from matching.models import *
class UserLogInSerializer(serializers.Serializer):

    email = serializers.CharField(max_length=255)
    password = serializers.CharField(min_length=4)


class UserRegisterSerializer(serializers.ModelSerializer):

	class Meta:
		model = Account
		fields = ('email','password','first_name','last_name','tel','address','is_driver','personal_id','license')


class UserRequestSerializer(serializers.ModelSerializer):

	class Meta:
		model = Request
		exclude = ('account',)

class UserTravelSerializer(serializers.ModelSerializer):

	class Meta:
		model = Travel
		fields = ('start_location','start_longtitude','car_id','start_lattitude','destination_location','destination_longtitude','destination_lattitude','current_longtitude','current_lattitude','is_complete')


class UseraddcarSerializer(serializers.ModelSerializer):
	class Meta:
		model = Car
		fields = ('license','_model','year','_type')	

class UserLogoutSerializer(serializers.Serializer):
	"""docstring for UserLogoutSerializer"""

		
class testSerializer(serializers.Serializer):
		"""sdgg"""


class UserMatchListSerializer(serializers.Serializer):
	class Meta:
		model = Matching_List
		fields = ('travel_id')
			
		"""sdgg"""
		
class UserMatchSerializer(serializers.ModelSerializer):
	class Meta:
		model = Matching
		fields = ('driver','customer','status')
	
			

		
			