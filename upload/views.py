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
    queryset = Signature.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = (FileSerializer,)
    parser_classes = (MultiPartParser, FormParser)
    def create(self, request):
        serializer = self.get_serializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
