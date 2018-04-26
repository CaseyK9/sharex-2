from django.shortcuts import render
from .form import DocumentForm
from rest_framework.response import Response
def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return Response("done")
    return Response("fail")
# Create your views here.
