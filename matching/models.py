from django.db import models
from django.utils import timezone, six
from django.conf import settings
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser, PermissionsMixin, Permission)
from django.contrib.auth.validators import UnicodeUsernameValidator, ASCIIUsernameValidator


class Matching(models.Model):
	travel_data = models.ForeignKey(settings.TRAVEL,blank=True,null=True)
	request_data = models.ForeignKey(settings.REQUEST,blank=True,null=True)

	status = models.CharField(max_length=255,default="doing")
	_next = models.IntegerField(blank=True,null=True,default=None)
	timestamp = models.DateTimeField(auto_now_add=True, db_index=True,null=True)
	timeupdate = models.DateTimeField(auto_now=True)
	
		