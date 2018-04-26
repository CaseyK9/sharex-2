from django import forms
from .models import Imageupload

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Imageupload
        fields = ('document', )