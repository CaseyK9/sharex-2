from django.db import models
from django.conf import settings

class Travel(models.Model):
	account = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
	start_location = models.CharField(max_length=255,blank=True,null=True)
	start_longtitude = models.FloatField(max_length=255,blank=True,null=True)
	start_lattitude = models.FloatField(max_length=255,blank=True,null=True)
	car_id = models.CharField(max_length=255,blank=True,null=True)
	destination_location = models.CharField(max_length=255,blank=True,null=True)
	destination_longtitude = models.FloatField(max_length=255,blank=True,null=True)
	destination_lattitude = models.FloatField(max_length=255,blank=True,null=True)

	current_longtitude = models.FloatField(max_length=255,blank=True,null=True)
	current_lattitude = models.FloatField(max_length=255,blank=True,null=True)
	
	is_complete = models.BooleanField(default=False)

	timestamp = models.DateTimeField(auto_now_add=True, db_index=True,null=True)
	timeupdate = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.account.email if self.account.email else ""
# Create your models here.
# Create your models here.
