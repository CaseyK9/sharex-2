from django.shortcuts import render
from account.permissions import IsDriverAccount

class GetTravelViewSet(mixins.CreateModelMixin,
					    viewsets.GenericViewSet):
	queryset = Travel.objects.all()
	serializer_class = UserRequestSerializer
	def create(self,request):
		if request.user.is_authenticated():
			serializer = self.get_serializer(data=request.data)
			if serializer.is_valid():
				var_request = Request.objects.create(
					account = request.user,
					start_location = serializer.data['pickup_location'],
					start_longtitude = serializer.data['pickup_longtitude'],
					start_lattitude = serializer.data['pickup_lattitude'],
					destination_location = serializer.data['destination_location'],
					destination_longtitude = serializer.data['destination_longtitude'],
					destination_lattitude = serializer.data['destination_lattitude'],
					current_longtitude = serializer.data['current_longtitude'],
					current_lattitude = serializer.data['current_lattitude'],
					is_complete = serializer.data['is_complete']
				)
				var_request.save()
			return JsonResponse({'error':'false','content':'success'})
		else :
			return Response("Unauthenticated")
# Create your views here.
