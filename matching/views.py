from django.shortcuts import render
from account.permissions import IsDriverAccount,IsAuthenticated
from rest_framework import viewsets, mixins
from request.models import Request
from travel.models import Travel
from urllib.request import urlopen
from .models import Matching
from .models import Matching_List
from account.serializers import UserMatchListSerializer,UserMatchSerializer,GetMatchingDetail
from rest_framework.response import Response
from django.core import serializers
from travel.models import Travel
from request.models import Request
from account.models import Account
import json

class GetMatching_Detail(mixins.CreateModelMixin,
					    viewsets.GenericViewSet):
	queryset = Matching.objects.all()
	serializer_class = GetMatchingDetail
	permission_classes = (IsDriverAccount,)
	def create(self,request):
		serializer = self.get_serializer(data = request.data)
		if serializer.is_valid():
			mc = Matching.objects.get(pk = serializer.data['matching_id'])
			if mc != None:
				detail = {'travel':[],'request':[]}
				#name = rq.account.first_name+" "+rq.account.last_name
				name = mc.request_data.account.first_name+" "+mc.request_data.account.last_name
				detail['travel'].append({'travel_id':mc.travel_data.pk,'start_location':mc.travel_data.start_location,'start_longtitude':mc.travel_data.start_longtitude,'start_lattitude':mc.travel_data.start_lattitude,'car_id':mc.travel_data.car_id,'destination_location':mc.travel_data.destination_location,'destination_longtitude':mc.travel_data.destination_longtitude,'destination_lattitude':mc.travel_data.destination_lattitude,'status':mc.travel_data.status})
				detail['request'].append({'request_id':mc.request_data.pk,'pickup_location':mc.request_data.pickup_location,'pickup_longtitude':mc.request_data.pickup_longtitude,'pickup_lattitude':mc.request_data.pickup_lattitude,'receiver_name':mc.request_data.receiver_name,'receiver_tel':mc.request_data.receiver_tel,'receiver_address':mc.request_data.receiver_address,'destination_location':mc.request_data.destination_location,'destination_longtitude':mc.request_data.destination_longtitude,'destination_lattitude':mc.request_data.destination_lattitude,'status':mc.request_data.status,'_type':mc.request_data._type,'fare':mc.request_data.fare,'customer_name':name,'customer_tel':mc.request_data.account.tel,'address':mc.request_data.account.address})
				return Response(detail)
			else:
				return Response({'error':True,'content' : 'failed'},status=status.HTTP_400_BAD_REQUEST)


class GetMatchViewSet(mixins.CreateModelMixin,
					    viewsets.GenericViewSet):
	queryset = Matching.objects.all()
	serializer_class = UserMatchSerializer
	permission_classes = (IsDriverAccount,IsAuthenticated,)
	def create(self,request):
		serializer = self.get_serializer(data=request.data)
		if serializer.is_valid():
			travel_obj = Travel.objects.get(pk = serializer.data['travel'])
			travel_obj.account.status = "busy"
			travel_obj.account.save()
			request_obj = Request.objects.get(pk = serializer.data['request'])
			var_request = Matching.objects.create(
				travel_data = travel_obj,
				request_data = request_obj,
				#lumbub = 
			).save()

			print(var_request)
			return Response("done")
		else:
			return Response({'error':True,'content' : 'failed'},status=status.HTTP_400_BAD_REQUEST)