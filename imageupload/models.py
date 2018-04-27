from django.db import models
from django.utils import timezone, six
from django.conf import settings
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser, PermissionsMixin, Permission)
from django.contrib.auth.validators import UnicodeUsernameValidator, ASCIIUsernameValidator
class Imageupload(models.Model):
	image = models.ImageField(upload_to="signature",blank=False, null=True)
	rating = models.FloatField(default=0,blank=True,null=True)
	request_id = models.IntegerField(default=0,blank=True,null=True)