from django.shortcuts import render
from account.permissions import IsDriverAccount,IsAuthenticated
from rest_framework import viewsets, mixins
from request.models import Request
from travel.models import Travel
from urllib.request import urlopen
from .models import Matching
from account.serializers import UserMatchListSerializer,UserMatchSerializer,GetMatchingDetail,GetMultipleMatching,GetMultipleMatching_Sub,UpdateMatchingStation,StoreRouteUrl,MakeItDone,TestImg
from rest_framework.response import Response
from django.core import serializers
from travel.models import Travel
from request.models import Request
from account.models import Account
from matching_detail.models import Matching_Detail
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
			response_message = {'matching_id':[],'travel_id':[],'tracking_key':[],'current_station':[],'sequence':[],'details':[],'travel_point':{'start':{'lat':mc.travel_data.start_lattitude,'long':mc.travel_data.start_longtitude},'end':{'lat':mc.travel_data.destination_lattitude,'long':mc.travel_data.destination_longtitude}}}
			response_message['matching_id'].append(serializer.data['matching_id'])
			response_message['travel_id'].append(mc.travel_data.pk)
			response_message['current_station'].append(mc.current_station)
			if mc != None:
				for i in range(0,len(mc.sequence.split('->'))-1,1):
					rq_id = int(mc.sequence.split('->')[i][0:len(mc.sequence.split('->')[i])-2])
					tmp = Request.objects.get(pk=rq_id)
					if i == 0:
						response_message['tracking_key'].append(tmp.tracking_key)
					if mc.sequence.split('->')[i][len(mc.sequence.split('->')[i])-2] == 'a':
						response_message['sequence'].append({'request_id':rq_id,'status':'pickup'})
					if mc.sequence.split('->')[i][len(mc.sequence.split('->')[i])-2] == 'b':
						response_message['sequence'].append({'request_id':rq_id,'status':'dropoff'})
						response_message['details'].append({'request_id':tmp.pk,'customer_name':tmp.account.first_name,'customer_tel':tmp.account.tel,'pickup_location':tmp.pickup_location,'pickup_longtitude':tmp.pickup_longtitude,'pickup_lattitude':tmp.pickup_lattitude,'destination_location':tmp.destination_location,'destination_longtitude':tmp.destination_longtitude,'destination_lattitude':tmp.destination_lattitude,'receiver_name':tmp.receiver_name,'receiver_tel':tmp.receiver_tel,'receiver_address':tmp.receiver_address,'type':tmp._type,'fare':tmp.fare})
				return Response(response_message)
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
		print("test")
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
							return Response({'status':'Unavailable request'})
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
					#mc_dt_obj = Matching_Detail.objects.create(
					#	matching = var_matching.pk,
					#	travel =travel_obj,
					#	request = tmp,
					#)
					#mc_dt = Matching_Detail.objects.create(
					#	matching = var_matching,
					#	travel = travel_obj,
					#	request = tmp,
					#	status = 'matched'
					#)
					tmp.status = "matched"
					tmp.tracking_key = serializer.data['tracking_key']
					tmp.save()
					url = 'https://fcm.googleapis.com/fcm/send'
					#print(type(tmp.account.firebase_key)+tmp.account.first_name)
					payload = '{"to":"'+tmp.account.firebase_key+'","data":{},"notification":{"title":"Your request has been matched","body":"idontknow","priority":"high","sound":"default"},}'
					#print(payload)
					headers = {'Content-Type':"application/json",'Authorization':"key=AAAAlRsX6G8:APA91bHeUES-WUYy2bYSLzbK6td4p8xZACl_LunpyDmLEtffHD_MYkJrDii5XdfhTDX27Vr1m9YwrFL7NhJtdVHUJENur3Zf5IRD5zKduM1MH_d49zrGz77u9r6DaT2erz_Nayp_izfp"}
					r = requests.post(url,data=payload,headers=headers)
					
				travel_obj.account.status = "busy"
				print(travel_obj.account.status)
				travel_obj.account.save()
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
			mc_obj = Matching.objects.get(pk=serializer.data['matching_id'])
			if mc_obj.travel_data.status == 'done':
				return Response("This matching has been finished")
			if mc_obj.current_station < len(mc_obj.sequence.split('->'))-2:
				mc_obj.current_station = mc_obj.current_station+1;
				mc_obj.save()
				if mc_obj.sequence.split('->')[mc_obj.current_station-1][len(mc_obj.sequence.split('->')[mc_obj.current_station-1])-2] == 'b':
					rq_obj = Request.objects.get(pk = int(mc_obj.sequence.split('->')[mc_obj.current_station-1][0:len(mc_obj.sequence.split('->')[mc_obj.current_station-1])-2]))
					print("done")
					rq_obj.status = 'done'
					rq_obj.save()
					return Response("dropoff done")
				else:
					return Response("pickup done")
			if mc_obj.current_station == len(mc_obj.sequence.split('->'))-1: #success traveling
				mc_obj.travel_data.status = 'done';
				mc_obj.travel_data.account.status = 'free';
				#for i in range(0,len(mc_obj.sequence.split("->"))-1,1):
				#	rq_obj = Request.objects.filter(pk = int(mc_obj.sequence.split("->")[i][0:len(mc_obj.sequence.split("->")[i])-1]))
				#	rq_obj.status = 'done'
				#	rq_obj.save()
				mc_obj.travel_data.save()
				mc_obj.travel_data.account.save()
				return Response("travel completed")

		else:
			return Response("invalid serializer")
	


class Store_Route_Url(mixins.CreateModelMixin,
					    viewsets.GenericViewSet):
	queryset = Matching.objects.all()
	serializer_class = StoreRouteUrl
	permission_classes = (IsDriverAccount,)
	def create(self,request):
		serializer = self.get_serializer(data = request.data)
		if serializer.is_valid():
			rq_obj = Request.objects.get(pk = serializer.data['request_id'])
			rq_obj.route_url = serializer.data['route_url']
			rq_obj.save()
		else:
			return Response("invalid serializer")


class Make_It_Done(mixins.CreateModelMixin,
					    viewsets.GenericViewSet):
	queryset = Matching.objects.all()
	serializer_class = MakeItDone
	permission_classes = (IsDriverAccount,)
	def create(self,request):
		serializer = self.get_serializer(data = request.data)
		if serializer.is_valid():
			request.user.rating_sum += serializer.data['rating']
			request.user.rating_number += 1
			request.user.save()
			return Response("Done")
		else:
			return Response("invalid serializer")

class Test_Img(mixins.CreateModelMixin,
					    viewsets.GenericViewSet):
	queryset = Matching.objects.all()
	serializer_class = TestImg
	permission_classes = (IsDriverAccount,)
	def create(self,request):
		serializer = self.get_serializer(data = request.data)
		if serializer.is_valid():
			rq = Request.objects.get(pk = serializer.data['request_id'])
			rq.signature = serializer.data['img']
			rq.save()
			return Response("Done")
		else:
			return Response("invalid serializer")