from django.db import models
class Imageupload(models.Model):
  image = models.ImageField(blank=False, null=False)
  timestamp = models.DateTimeField(auto_now_add=True)