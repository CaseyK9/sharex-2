from django.db import models
class Signature(models.Model):
      image = models.ImageField(upload_to='signature',null=True)
      timestamp = models.DateTimeField(auto_now_add=True)
# Create your models here.
