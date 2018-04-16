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
	permission_classes = (IsDriverAccount,)
	def create(self,request):
		serializer = self.get_serializer(data = request.data)
		if serializer.is_valid():
			rq = Request.objects.get(pk = serializer.data['request_id'])
			if rq != None:
				detail = {'details':[],'status':[]}
				name = rq.account.first_name+" "+rq.account.last_name
				detail['details'].append({'request_id':rq.pk,'customer_name':name,'customer_tel':rq.account.tel,'pickup_location':rq.pickup_location,'pickup_longtitude':rq.pickup_longtitude,'pickup_lattitude':rq.pickup_lattitude,'destination_location':rq.destination_location,'destination_longtitude':rq.destination_longtitude,'destination_lattitude':rq.destination_lattitude,'receiver_name':rq.receiver_name,'receiver_tel':rq.receiver_tel,'receiver_address':rq.receiver_address,'type':rq._type,'fare':rq.fare})
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
			for i in Request.objects.all():
				if request.user == i.account:
					if i.status == "doing":
						rq_list.append({'request_id':i.pk,'pickup_location':i.pickup_location,'pickup_lattitude':i.pickup_lattitude,'pickup_longtitude':i.pickup_longtitude,'dropoff_address':i.destination_location,'dropoff_lattitude':i.destination_lattitude,'dropoff_longtitude':i.destination_longtitude,'receiver_address':i.receiver_address,'receiver_tel':i.receiver_tel,'fare':i.fare,'status':i.status,'timestamp':str(i.timestamp)})
			return Response(rq_list)