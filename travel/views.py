from django.shortcuts import render
from account.permissions import IsDriverAccount
from rest_framework import viewsets, mixins
from .models import Travel
from account.serializers import UserTravelSerializer,Travel_List_Serializer
from rest_framework.response import Response
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.core.serializers import serialize
import json
from django.http import JsonResponse
from request.models import Request
from urllib.request import urlopen



class GetTravel_List(mixins.CreateModelMixin,
					    viewsets.GenericViewSet):
	queryset = Travel.objects.all()	
	serializer_class = Travel_List_Serializer
	permission_classes = (IsDriverAccount,)
	def create(self,request):
		if request.user.is_authenticated():
			serializer = self.get_serializer(data=request.data)
			if serializer.is_valid():
				#tv_list = Travel.objects.get(account = request.user)
				#json_res = json.loads(tv_list)
				#data = serializers.serialize("xml", Travel.objects.filter(account = request.user))
				travel = Travel.objects.filter(account=request.user)		
				response = Travel_List_Serializer(travel, many=True).data
				return Response(response)
				#data = serialize('json', Travel.objects.filter(account = request.user))
				#return JsonResponse(json.dumps(data),safe = False)
		else :
			return Response(status=400)

class GetTravelViewSet(mixins.CreateModelMixin,
					    viewsets.GenericViewSet):
	queryset = Travel.objects.all()
	serializer_class = UserTravelSerializer
	permission_classes = (IsDriverAccount,)
	def create(self,request):
		if request.user.is_authenticated():
			serializer = self.get_serializer(data=request.data)
			if serializer.is_valid():
				tv = Travel.objects.create(
					account = request.user,
					car_id = serializer.data['car_id'],
					start_location = serializer.data['start_location'],
					start_longtitude = serializer.data['start_longtitude'],
					start_lattitude = serializer.data['start_lattitude'],
					destination_location = serializer.data['destination_location'],
					destination_longtitude = serializer.data['destination_longtitude'],
					destination_lattitude = serializer.data['destination_lattitude'],
					current_longtitude = serializer.data['current_longtitude'],
					current_lattitude = serializer.data['current_lattitude'],
					status = serializer.data['status']
				)
				tv.save()
				LIST = {'details':[],'status':[]}
				sort_list = []
				tmp_list = []
				#return Response(LIST)
				j = 0
				k = 0
				#return Response(len(Request.objects.all()))
				for i in Request.objects.all():
					j+=1
					url = "https://maps.googleapis.com/maps/api/directions/json?origin="+str(tv.start_lattitude)+","+str(tv.start_longtitude)+"&destination="+str(tv.destination_lattitude)+","+str(tv.destination_longtitude)+"&waypoints=via:"+str(i.pickup_lattitude)+","+str(i.pickup_longtitude)+"|via:"+str(i.destination_lattitude)+","+str(i.destination_longtitude)+"&key=AIzaSyD8j1ghThaDbCn_8FNv2CtXqAmMNSLje8M"
					response = urlopen(url).read()
					json_res = json.loads(response)
					if json_res["status"] == "OK":
						distance = json_res["routes"][0]["legs"][0]["distance"]["value"]/1000
						sort_list.append([k,distance])
						k+=1
						pickup = i.pickup_location.split(",")
						destination = i.destination_location.split(",")
						if len(pickup) >= 2:
							temp_pickup = pickup[0]+pickup[1]
						else:
							temp_pickup = pickup[0]
						if len(destination) >= 2:
							temp_destination = destination[0]+destination[1]
							temp_destination.replace(",","\n")
						else:
							temp_destination = destination[0]
						tmp_list.append({'travel_id':tv.pk,'request_id':i.pk,'pickup_location':temp_pickup,'destination_location':temp_destination,'distance':distance,'fare':i.fare,'account_id':i.account.pk})
						#return Response(distance)
						
						#return Response(json.dumps(LIST[j]))
						#LIST.append([tv.pk,i.pk,distance])
					#return Response(distance)
				if len(sort_list)==0:
					LIST['status'].append({'status':'no request'})
				else:
					sort_list = sorted(sort_list, key=lambda x: x[1])
					for i in range(0,k):
						if i<5:
							LIST['details'].append(tmp_list[sort_list[i][0]])
					LIST['status'].append({'status': 'okay'})
				return Response(LIST)

			return Response(json_res)	
			return Response({'error':'false','content':'success'})
		else :
			return Response("Unauthenticated")
# Create your views here.
