from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from account.serializers import ImageUpload
from request.models import Request
class Image_Upload(APIView):
	parser_classes = (MultiPartParser, FormParser)
	def post(self, request, *args, **kwargs):
		file_serializer = ImageUpload(data=request.FILES)
		serializer = ImageUpload(data=request.data)
		#rq = Request.objects.get()
		if file_serializer.is_valid():
			#print(file_serializer.data.)
			#file_serializer.save()
			return Response(serializer.data['request_id'], status=status.HTTP_201_CREATED)
		else:
			return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)