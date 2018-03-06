from django.shortcuts import render
from account.permissions import IsDriverAccount
from rest_framework import viewsets, mixins
from .models import Travel
from account.serializers import UserTravelSerializer
from rest_framework.response import Response
class GetTravelViewSet(mixins.CreateModelMixin,
					    viewsets.GenericViewSet):
	queryset = Travel.objects.all()
	serializer_class = UserTravelSerializer
	permission_classes = (IsDriverAccount,)
	def create(self,request):
		if request.user.is_authenticated():
			serializer = self.get_serializer(data=request.data)
			if serializer.is_valid():
				var_request = Travel.objects.create(
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
					is_complete = serializer.data['is_complete']
				)
				var_request.save()
			return Response({'error':'false','content':'success'})
		else :
			return Response("Unauthenticated")
# Create your views here.
