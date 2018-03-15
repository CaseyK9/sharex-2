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

# Create your views here.

class GetList_Match_ViewSet(mixins.CreateModelMixin,viewsets.GenericViewSet): #retrive travel_number
	queryset = Matching_List.objects.all()
	serializer_class = UserMatchListSerializer
	permission_classes = (IsDriverAccount,IsAuthenticated,)	
	def create(self,request):
		serializer = self.get_serializer(data=request.data)
		if serializer.is_valid():
			#travel_id = serializer.data['travel_id']
			tv = Travel.objects.get(pk = serializer.data['travel_id'])
			#return Response(tv.pk)
			#dt = Request.objects.get(pk='6')
			LIST = []
			for i in Request.objects.all():
				url = "https://maps.googleapis.com/maps/api/directions/json?origin="+str(tv.start_lattitude)+","+str(tv.start_longtitude)+"&destination="+str(tv.destination_lattitude)+","+str(tv.destination_longtitude)+"&waypoints=via:"+str(i.pickup_lattitude)+","+str(i.pickup_longtitude)+"|via:"+str(i.destination_lattitude)+","+str(i.destination_longtitude)+"&key=AIzaSyD8j1ghThaDbCn_8FNv2CtXqAmMNSLje8M"
				response = urlopen(url).read()
				json_res = json.loads(response)
				#if json_res["status"] == "OK":
				#	return Response("hi")
				if json_res["status"] == "OK":
					distance = json_res["routes"][0]["legs"][0]["distance"]["value"]/1000
					#return Response(distance)
					LIST.append([tv.pk,i.pk,distance])
				#return Response(distance)
			LIST = sorted(LIST, key=lambda x: x[2])
			return Response(LIST)
		"""obj = Request.objects.all()
								tmp=[]
								url = "https://maps.googleapis.com/maps/api/directions/json?origin=75+9th+Ave+New+York,+NY&destination=MetLife+Stadium+1+MetLife+Stadium+Dr+East+Rutherford,+NJ+07073&key=AIzaSyD8j1ghThaDbCn_8FNv2CtXqAmMNSLje8M"
								response = urlopen(url).read()
								json_res = json.loads(response)
								json_res = json_res["routes"][0]["legs"][0]["distance"]["value"]/1000"""

		return Response(json_res)	
	"""for t in data:
		origin = str(t.pickup_lattitude)+","+str(t.pickup_longtitude)
		destination = str(t.destination_lattitude)+","+str(t.destination_longtitude)
		url = "https://maps.googleapis.com/maps/api/directions/json?origin="+origin+",+&destination="+destination+"&key=AIzaSyD8j1ghThaDbCn_8FNv2CtXqAmMNSLje8M"
		response = urlopen(url).read()"""


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