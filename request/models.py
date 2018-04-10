from django.db import models
from django.conf import settings
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser, PermissionsMixin, Permission)
from django.contrib.auth.validators import UnicodeUsernameValidator, ASCIIUsernameValidator
from django.utils import timezone, six
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from datetime import timedelta

class Request(models.Model):
	account = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
	pickup_location = models.CharField(max_length=255,blank=True,null=True)
	pickup_longtitude = models.FloatField(max_length=255,blank=True,null=True)
	pickup_lattitude = models.FloatField(max_length=255,blank=True,null=True)
	
	destination_location = models.CharField(max_length=255,blank=True,null=True)
	destination_longtitude = models.FloatField(max_length=255,blank=True,null=True)
	destination_lattitude = models.FloatField(max_length=255,blank=True,null=True)

	receiver_name = models.CharField(max_length=255,blank=True,null=True)
	receiver_tel = models.CharField(max_length=255,blank=True,null=True)
	receiver_address = models.CharField(max_length=255,blank=True,null=True)
	
	TYPE_CHOICES = (
		(1, 'truck'),
		(2, 'sedan'),
		(3, 'pickup'),
		(4, 'motorcycle'),
	)

	_type = models.PositiveSmallIntegerField(choices=TYPE_CHOICES , default='1')
	status = models.CharField(max_length=255,default="doing")
	fare = models.IntegerField(default = 0)
	expire_time = models.DateTimeField(_('expire'), default=timezone.now()+timezone.timedelta(days=1))

	def __str__(self):
		return self.account.email if self.account.email else "" 
# Create your models here.
