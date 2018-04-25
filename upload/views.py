from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from account.serializers import FileSerializer
from account.permissions import IsCustomerAccount,IsDriverAccount,IsAuthenticated
from .models import Signature
from rest_framework import viewsets, mixins
class FileView(mixins.CreateModelMixin,
					    viewsets.GenericViewSet):
    #queryset = Signature.objects.all()
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser)
    def create(self, request):
        file_serializer = FileSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
