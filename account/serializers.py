from rest_framework import serializers
from rest_framework.serializers import raise_errors_on_nested_writes, model_meta
#from upload.models import Signature
from .models import Account
from request.models import Request
from car.models import Car
from travel.models import Travel
from matching.models import *
from imageupload.models import *
class UserLogInSerializer(serializers.Serializer):

    email = serializers.CharField(max_length=255)
    password = serializers.CharField(min_length=4)
    firebase_key = serializers.CharField(max_length=255)


class UserRegisterSerializer(serializers.ModelSerializer,serializers.Serializer):
	class Meta:
		model = Account
		fields = ('email','password','first_name','last_name','tel','address','is_driver','personal_id','license','car_type')


class UserRequestSerializer(serializers.ModelSerializer,serializers.Serializer):
	expire_date = serializers.IntegerField()
	class Meta:
		model = Request
		exclude = ('account','status','expire_time')

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

class UserMatchSerializer(serializers.Serializer):
	travel = serializers.IntegerField()
	request = serializers.IntegerField()


class GetMatchingDetail(serializers.Serializer):
	matching_id = serializers.IntegerField()


class GetRequestDetail(serializers.Serializer):
	request_id = serializers.IntegerField()

class GetMultipleMatching_Sub(serializers.Serializer):
	request_id = serializers.IntegerField()

class GetMultipleMatching(serializers.Serializer):
	#import GetMultipleMatching_Sub
	travel_id = serializers.IntegerField()
	tracking_key = serializers.CharField()
	request_list = GetMultipleMatching_Sub(many=True)

class UpdateMatchingStation(serializers.Serializer):
	#import GetMultipleMatching_Sub
	matching_id = serializers.IntegerField()

class GetRequestHistory(serializers.Serializer):
	"""adsfasdfasdfasdfasdf"""

class CancelRequest(serializers.Serializer):
	#import GetMultipleMatching_Sub
	request_id = serializers.IntegerField()


class StoreRouteUrl(serializers.Serializer):
	#import GetMultipleMatching_Sub
	request_id = serializers.IntegerField()
	route_url = serializers.CharField()


class GetAccountDetail(serializers.Serializer):
	"""adsfasdfasdfasdfasdf"""


class EditProfile(serializers.ModelSerializer):
	class Meta:
		model = Account
		fields = ('first_name','last_name','tel','address')


class MakeItDone(serializers.Serializer):
	rating = serializers.FloatField()

class GetDriverDetail(serializers.Serializer):
	"""asdfasdf"""

class ImageUpload(serializers.ModelSerializer):
	class  Meta():
		model = Imageupload
		fields = '__all__'

			

'''
class FileSerializer(serializers.ModelSerializer,serializers.Serializer):
    request_id = serializers.IntegerField()
    class Meta():
            model = Signature
            fields = ('image')'''
