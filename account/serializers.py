from rest_framework import serializers
from rest_framework.serializers import raise_errors_on_nested_writes, model_meta

from .models import Account
from request.models import Request
from car.models import Car
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
		fields = ('pickup_location','pickup_longtitude','pickup_lattitude','destination_location','destination_longtitude','destination_lattitude','_type','is_complete')


class UseraddcarSerializer(serializers.ModelSerializer):
	class Meta:
		model = Car
		fields = ('license','_model','year','_type')	

class UserLogoutSerializer(serializers.Serializer):
	"""docstring for UserLogoutSerializer"""

		
class testSerializer(serializers.Serializer):
		"""sdgg"""

# class genSerializer(serializers.Serializer):
# 	"""sdgg"""
		
			