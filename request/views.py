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
from account.models import Account
from .models import Request
from matching_detail.models import Matching_Detail
#from .authenticate import CsrfExemptSessionAuthentication
from account.serializers import *
from account.permissions import IsCustomerAccount,IsDriverAccount

class GetRequestViewSet(mixins.CreateModelMixin,
					    viewsets.GenericViewSet):
	queryset = Request.objects.all()
	serializer_class = UserRequestSerializer
	permission_classes = (IsCustomerAccount,)

	def create(self,request):
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
				#status = serializer.data['status'],
				fare = serializer.data['fare'],
				expire_time = timezone.now()+timezone.timedelta(days=serializer.data['expire_date'])
			).save()
			print(var_request)
			return Response(({'error':False,'content':'success'}))
		else:
			return Response({'error':True,'content' : 'failed'},status=status.HTTP_400_BAD_REQUEST)


class Get_Request_Detail(mixins.CreateModelMixin,
					    viewsets.GenericViewSet):
	queryset = Request.objects.all()
	serializer_class = GetRequestDetail
	permission_classes = (IsAuthenticated,)
	def create(self,request):
		serializer = self.get_serializer(data = request.data)
		if serializer.is_valid():
			rq = Request.objects.get(pk = serializer.data['request_id'])
			mc_dt = Matching_Detail.objects.get(request = rq)
			if rq != None:
				detail = {'request_details':[],'driver_detials':[],'status':[]}
				name = rq.account.first_name+" "+rq.account.last_name
				#pickup_address = rq.pickup_location.split(',',1)[0]
				#destination_address = rq.destination_location.split(',',1)[0]
				detail['request_details'].append({'request_id':rq.pk,'customer_name':name,'customer_tel':rq.account.tel,'pickup_location':rq.pickup_location,'pickup_longtitude':rq.pickup_longtitude,'pickup_lattitude':rq.pickup_lattitude,'destination_location':rq.destination_location,'destination_longtitude':rq.destination_longtitude,'destination_lattitude':rq.destination_lattitude,'receiver_name':rq.receiver_name,'receiver_tel':rq.receiver_tel,'receiver_address':rq.receiver_address,'type':rq._type,'fare':rq.fare,'tracking_key':rq.tracking_key,'route_url':rq.route_url})
				if mc_dt != None:
					ac = mc_dt.travel.account
					detail['driver_detials'].append({'name':ac.first_name+" "+ac.last_name,'tel':ac.tel,'license':ac.license,'rating':rating_sum/rating_number})
				detail['status'].append({'status':'okay'})
				return Response(detail)
			else:
				return


class Get_Request_History(mixins.CreateModelMixin,
					    viewsets.GenericViewSet):
	queryset = Request.objects.all()
	serializer_class = GetRequestHistory
	permission_classes = (IsCustomerAccount,)
	def create(self,request):
		serializer = self.get_serializer(data = request.data)
		if serializer.is_valid():
			rq_list = []
			#obj = Token.objects.get(user=user)
			for i in Request.objects.all():
				if request.user == i.account:
					#if i.status == "doing":
					text = str(i.timestamp).split('.',1)[0]
					text_date = text.split(' ',1)[0]
					text_date = text_date.split('-')
					tmp = text_date[0]
					text_date[0]=text_date[2]
					text_date[2]=tmp
					text_date = text_date[0]+'-'+text_date[1]+'-'+text_date[2]
					text_time = text.split(' ',1)[1]
					pickup_address = i.pickup_location.split(',',1)[0]
					destination_address = i.destination_location.split(',',1)[0]
					rq_list.append({'request_id':i.pk,'pickup_location':pickup_address,'pickup_lattitude':i.pickup_lattitude,'pickup_longtitude':i.pickup_longtitude,'dropoff_address':destination_address,'dropoff_lattitude':i.destination_lattitude,'dropoff_longtitude':i.destination_longtitude,'receiver_address':i.receiver_address,'receiver_tel':i.receiver_tel,'fare':i.fare,'status':i.status,'timestamp':text_date+' '+text_time,'_type':i._type})
			return Response(rq_list)


class Cancel_Request(mixins.CreateModelMixin,
					    viewsets.GenericViewSet):
	queryset = Request.objects.all()
	serializer_class = CancelRequest
	permission_classes = (IsCustomerAccount,)
	def create(self,request):
		serializer = self.get_serializer(data = request.data)
		if serializer.is_valid():
			rq = Request.objects.get(pk = serializer.data['request_id'])
			if rq.status=='doing':
				rq.status = "cancelled"
				rq.save()
				return Response("success")
			elif rq.status == 'matched':
				return Response("Request has already matched")

		
class Get_RequestxDriver_Detail(mixins.CreateModelMixin,
					    viewsets.GenericViewSet):
	queryset = Request.objects.all()
	serializer_class = GetRequestxDriverDetail
	permission_classes = (IsAuthenticated,)
	def create(self,request):
		serializer = self.get_serializer(data = request.data)
		if serializer.is_valid():
			rq = Request.objects.get(pk = serializer.data['request_id'])
			mc_dt = Matching_Detail.objects.get(request = rq)
			return Response(mc_dt.pk)
		else:
			return Response("invalid serializer")