from rest_framework import serializers
from rest_framework.serializers import raise_errors_on_nested_writes, model_meta

from .models import Account

class UserLogInSerializer(serializers.Serializer):

    email = serializers.CharField(max_length=255)
    password = serializers.CharField(min_length=4)


class UserRegisterSerializer(serializers.ModelSerializer):

	class Meta:
		model = Account
		fields = ('email','password','first_name','last_name','tel','address','is_driver','personal_id','license')

class UserLogoutSerializer(serializers.Serializer):
	"""docstring for UserLogoutSerializer"""

		
class testSerializer(serializers.Serializer):
		"""sdgg"""

# class genSerializer(serializers.Serializer):
# 	"""sdgg"""
		
			