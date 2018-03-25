from django.shortcuts import render
from account.permissions import IsDriverAccount,IsAuthenticated
from rest_framework import viewsets, mixins
from request.models import Request
from travel.models import Travel
from urllib.request import urlopen
from .models import Matching
from .models import Matching_List
from account.serializers import UserMatchListSerializer,UserMatchSerializer
from rest_framework.response import Response
from django.core import serializers
import json

class GetMatchViewSet(mixins.CreateModelMixin,
					    viewsets.GenericViewSet):
	queryset = Matching.objects.all()
	serializer_class = UserMatchSerializer
	permission_classes = (IsDriverAccount,IsAuthenticated,)
	def create(self,request):
		serializer = self.get_serializer(data=request.data)
		if serializer.is_valid():
			var_request = Matching.objects.create(
				driver = serializer.data['driver'],
				customer = serializer.data['customer'],
			).save()
			print(var_request)
			return Response("done")
		else:
			return Response({'error':True,'content' : 'failed'},status=status.HTTP_400_BAD_REQUEST)