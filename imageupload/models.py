from django.db import models
class Imageupload(models.Model):
    document = models.ImageField(upload_to='signature')
    uploaded_at = models.DateTimeField(auto_now_add=True)
# Create your models here.
