from django.shortcuts import render
from account.permissions import IsDriverAccount,IsAuthenticated
from rest_framework import viewsets, mixins
from request.models import Request
from travel.models import Travel
from urllib.request import urlopen
from .models import Matching
from account.serializers import UserMatchListSerializer,UserMatchSerializer,GetMatchingDetail,GetMultipleMatching,GetMultipleMatching_Sub
from rest_framework.response import Response
from django.core import serializers
from travel.models import Travel
from request.models import Request
from account.models import Account
import json
import requests

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
				#name = tmp.account.first_name+" "+tmp.account.last_name
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



class Get_Multiple_Matching(mixins.CreateModelMixin,
					    viewsets.GenericViewSet):
	queryset = Matching.objects.all()
	serializer_class = GetMultipleMatching
	permission_classes =  (IsDriverAccount,IsAuthenticated,)
	def create(self,request):
		serializer = self.get_serializer(data=request.data)
		if serializer.is_valid():
			location=[]
			response_message = {'matching_id':[],'travel_id':[],'sequence':[],'details':[]}
			travel_obj = Travel.objects.get(pk = serializer.data['travel_id'])
			if travel_obj.account.status == "busy":
				return Response({'status':'Driver is busy'})
			j = len(serializer.data['request_list'])
			if j==0:
				return Response({'status':'no list'})
			else:
				response_message['travel_id'].append(travel_obj.pk)
				for i in range(0,j+1,1):
					if i==0:
						tmp = Travel.objects.get(pk = serializer.data['travel_id'])
						location.append({'address':'start','lat':str(tmp.start_lattitude),'lng':str(tmp.start_longtitude)})
					if i==j:
						tmp = Travel.objects.get(pk = serializer.data['travel_id'])
						location.append({'address':'stop','lat':str(tmp.destination_lattitude),'lng':str(tmp.destination_longtitude)})
					else:
						tmp = Request.objects.get(pk = serializer.data['request_list'][i]['request_id'])
						response_message['details'].append({'request_id':tmp.pk,'customer_name':tmp.account.first_name,'customer_tel':tmp.account.tel,'pickup_location':tmp.pickup_location,'pickup_longtitude':tmp.pickup_longtitude,'pickup_lattitude':tmp.pickup_lattitude,'destination_location':tmp.destination_location,'destination_longtitude':tmp.destination_longtitude,'destination_lattitude':tmp.destination_lattitude,'receiver_name':tmp.receiver_name,'receiver_tel':tmp.receiver_tel,'receiver_address':tmp.receiver_address,'type':tmp._type,'fare':tmp.fare})
						if tmp.status == "matched":
							return Response({'status'='Unavailable request'})
						location.append({'address':str(tmp.pk)+"a0",'lat':str(tmp.pickup_lattitude),'lng':str(tmp.pickup_longtitude)})
						location.append({'address':str(tmp.pk)+"b0",'lat':str(tmp.destination_lattitude),'lng':str(tmp.destination_longtitude),'restrictions':{'after':(i*2)+1}})
				url = 'https://api.routexl.nl/tour/'
				payload = {'locations':json.dumps(location)}
				headers = {'Authorization':"Basic c2hhcmV4c2VydmVyOnNoYXJleGFkbWlu"}
				r = requests.post(url, data=payload, headers=headers)
				temp = json.loads(r.text)
				message = ""

				for i in range(1,temp['count']-1,1):
					if temp['route'][str(i)]['name'][len(temp['route'][str(i)]['name'])-2] == 'a':
						rq_id = int(temp['route'][str(i)]['name'][:(len(temp['route'][str(i)]['name'])-2)])
						response_message['sequence'].append({'request_id':rq_id,'status':'pickup','complete':False})
					elif temp['route'][str(i)]['name'][len(temp['route'][str(i)]['name'])-2] == 'b':
						rq_id = int(temp['route'][str(i)]['name'][:(len(temp['route'][str(i)]['name'])-2)])
						response_message['sequence'].append({'request_id':rq_id,'status':'dropoff','complete':False})
					message = message+temp['route'][str(i)]['name']+"->"


				
				var_matching = Matching.objects.create(
					travel_data = travel_obj,
					sequence = message
				)
				for i in range(0,len(serializer.data['request_list']),1):
					tmp = Request.objects.get(pk = serializer.data['request_list'][i]['request_id'])
					mc_dt = Matching_Detail.objects.create(
						matching = var_matching,
						travel = travel_obj,
						request = tmp,
						status = 'matched'
					)
					tmp.status = "matched"
					tmp.save()

				travel_obj.account.status = "busy"
				travel_obj.save()
				#tt = Matching.objects.filter(travel_data = travel_obj,sequence = message)
				response_message['matching_id'].append(var_matching.pk)
				return Response(response_message)
			return Response(json.loads(r.text))
		else: return Response({'status':'serializer unvalid'})


class Update_Matching_Station(mixins.CreateModelMixin,viewsets.GenericViewSet):
	queryset = Matching.objects.all()
	serializer_class = UpdateMatchingStation
	permission_classes = (IsDriverAccount,IsAuthenticated,)
	def create(self,request):
		serializer = self.get_serializer(data=request.data)
		if serializer.is_valid():
			mc_obj = Matching.objects.filter(pk = serializer.data['matching_id'])
			if mc_obj.current_station == len(mc_obj.sequence.split('->')-1): #success traveling
				mc_obj.travel_data.status = 'done';
				mc_obj.travel_data.account.status = 'free';
				for i in range(0,len(mc_obj.sequence.split("->"))-1,1):
					rq_obj = Request.objects.filter(pk = int(mc_obj.sequence.split("->")[i][0:len(mc_obj.sequence.split("->")[i])-1]))
					rq_obj.status = 'done'
					rq_obj.save()
				mc_obj.save()
			elif mc_obj.current_station == 0:
				mc_obj.current_station = mc_obj.current_station+1;
				mc_obj.save()
	
		