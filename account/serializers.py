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
		fields = ('email','password','first_name','last_name','tel','address','is_driver','personal_id','license','status')


class UserRequestSerializer(serializers.ModelSerializer):

	class Meta:
		model = Request
		exclude = ('account',)

class UserTravelSerializer(serializers.ModelSerializer):

	class Meta:
		model = Travel
		fields = ('start_location','start_longtitude','car_id','start_lattitude','destination_location','destination_longtitude','destination_lattitude','current_longtitude','current_lattitude','status')


class UseraddcarSerializer(serializers.ModelSerializer):
	class Meta:
		model = Car
		fields = ('license','_model','year','_type')	

class UserLogoutSerializer(serializers.Serializer):
	"""docstring for UserLogoutSerializer"""

		
class testSerializer(serializers.Serializer):
		"""sdgg"""


class UserMatchListSerializer(serializers.Serializer):
	travel_id = serializers.IntegerField()

class Travel_List_Serializer(serializers.ModelSerializer):
	class Meta:
		model = Travel
		fields= '__all__'

class UserMatchSerializer(serializers.ModelSerializer):
	class Meta:
		model = Matching
		fields = ('driver','customer','status')
	
			
class GetRequestDetail(serializers.Serializer):
	request_id = serializers.IntegerField()
		
		
			