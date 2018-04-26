from django.db import models
class Imageupload(models.Model):
  image = models.ImageField(upload_to="signature",blank=False, null=False)