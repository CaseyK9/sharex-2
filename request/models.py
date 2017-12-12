from django.db import models
from django.conf import settings
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser, PermissionsMixin, Permission)
from django.contrib.auth.validators import UnicodeUsernameValidator, ASCIIUsernameValidator
from django.utils import timezone, six
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

class Request(models.Model):
	account = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
	pickup_location = models.CharField(max_length=255,blank=True,null=True)
	pickup_longtitude = models.FloatField(max_length=255,blank=True,null=True)
	pickup_lattitude = models.FloatField(max_length=255,blank=True,null=True)
	
	destination_location = models.CharField(max_length=255,blank=True,null=True)
	destination_longtitude = models.FloatField(max_length=255,blank=True,null=True)
	destination_lattitude = models.FloatField(max_length=255,blank=True,null=True)
	
	TYPE_CHOICES = (
    	(1, 'truck'),
    	(2, 'pickup'),
    	(3, 'van'),
    	(4, 'eco_car'),
    	(5, 'SUV'),
    	(6, 'sport_car'),
    	(7, 'pickup'),
    )

	_type = models.PositiveSmallIntegerField(choices=TYPE_CHOICES , default='1')
	is_complete = models.BooleanField(default=False)

	timestamp = models.DateTimeField(auto_now_add=True, db_index=True,null=True)
	timeupdate = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.account.email if self.account.email else ""
# Create your models here.
