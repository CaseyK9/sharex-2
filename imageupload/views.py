from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser,JSONParser
from rest_framework.response import Response
from rest_framework import status
from account.serializers import ImageUpload
from request.models import Request
from travel.models import *
from matching_detail.models import *
from account.models import *
from matching.models import *
class Image_Upload(APIView):
	parser_classes = (MultiPartParser, FormParser)
	def post(self, request, *args, **kwargs):
		file_serializer = ImageUpload(data=request.data)
		#rq = Request.objects.get()
		if file_serializer.is_valid():
			#print(file_serializer.data.)
			file_serializer.save()
			print(file_serializer)
			rq = Request.objects.get(pk = file_serializer[2])
			mc = Matching_Detail.objects.get(request = rq)
			mc_obj = Matching.objects.get(pk=mc.matching_id)
			if mc_obj.travel_data.status == 'finished':
				return Response("This matching has been finished")
			if mc_obj.current_station < len(mc_obj.sequence.split('->'))-2:
				mc_obj.current_station = mc_obj.current_station+1;
				mc_obj.save()
				if mc_obj.sequence.split('->')[mc_obj.current_station-1][len(mc_obj.sequence.split('->')[mc_obj.current_station-1])-2] == 'b':
					rq_obj = Request.objects.get(pk = int(mc_obj.sequence.split('->')[mc_obj.current_station-1][0:len(mc_obj.sequence.split('->')[mc_obj.current_station-1])-2]))
					print("done")
					rq_obj.status = 'finished'
					rq_obj.signature = file_serializer.image
					rq_obj.save()
					mc_obj.travel_data.account.rating_sum += file_serializer.rating
					mc_obj.travel_data.account.rating_number += 1
					mc_obj.travel_data.account.save()
					return Response("dropoff done")
				else:
					return Response("pickup done")
			if mc_obj.current_station == len(mc_obj.sequence.split('->'))-1: #success traveling
				mc_obj.travel_data.status = 'finished'
				mc_obj.travel_data.account.status = 'free'
				mc_obj.travel_data.save()
				mc_obj.travel_data.account.save()
				return Response("travel completed")
			return Response(file_serializer.data, status=status.HTTP_201_CREATED)
		else:
			return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)