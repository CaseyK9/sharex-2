from django.db import models
class Imageupload(models.Model):
	image = models.ImageField(upload_to="signature",blank=False, null=False)
	rating = models.FloatField(default=0,blank=True,null=True)
	matching_id = models.IntegerField(default=0,blank=True,null=True)