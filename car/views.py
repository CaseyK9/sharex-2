from django.shortcuts import render
from .models import Car
from django.contrib.auth import authenticate, login, logout
from rest_framework import viewsets, mixins
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication,BasicAuthentication, SessionAuthentication
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied, NotAuthenticated
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.http import JsonResponse
from account.models import Account
from account.permissions import IsDriverAccount
from account.serializers import *

class add_car(mixins.CreateModelMixin,viewsets.GenericViewSet):
	queryset = Car.objects.all()
	serializer_class = UseraddcarSerializer
	permission_classes = (IsDriverAccount,)
	def create(self,request):
		serializer = self.serializer_class(data=request.data)
		if serializer.is_valid():
			_car = Car.objects.create(
				account = request.user,
				license = serializer.data['license'],
				_model = serializer.data['_model'],
				year = serializer.data['year'],
				_type = serializer.data['_type'],
		    ).save()
			return Response("done")
		return Response("Fail")
# Create your views here.
