from django.contrib.auth import authenticate, login, logout
from rest_framework import viewsets, mixins
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication,BasicAuthentication, SessionAuthentication
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied, NotAuthenticated
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.http import JsonResponse
from account.models import Account
from .models import Request
#from .authenticate import CsrfExemptSessionAuthentication
from account.serializers import *

class GetRequestViewSet(mixins.CreateModelMixin,
					    viewsets.GenericViewSet):
	queryset = Request.objects.all()
	serializer_class = UserRequestSerializer
	def create(self,request):
		if request.user.is_authenticated():
			serializer = self.get_serializer(data=request.data)
			if serializer.is_valid():
				var_request = Request.objects.create(
					account = request.user,
					pickup_location = serializer.data['pickup_location'],
					pickup_longtitude = serializer.data['pickup_longtitude'],
					pickup_lattitude = serializer.data['pickup_lattitude'],
					destination_location = serializer.data['destination_location'],
					destination_longtitude = serializer.data['destination_longtitude'],
					destination_lattitude = serializer.data['destination_lattitude'],
					receiver_name = serializer.data['receiver_name'],
					receiver_tel = serializer.data['receiver_tel'],
					receiver_address = serializer.data['receiver_address'],
					_type = serializer.data['_type'],
					is_complete = serializer.data['is_complete']
				)
				var_request.save()
			return JsonResponse({'error':'false','content':'success'})
		else :
			return Response("Unauthenticated")
			
# Create your views her