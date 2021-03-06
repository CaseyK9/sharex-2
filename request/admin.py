from django.contrib import admin
from .models import *


class RequestAdmin(admin.ModelAdmin):
	list_display = ('id', 'get_email', 'status')

	def get_email(self,request):
		return request.account.email if request.account else ""

	get_email.short_description = "Email"

admin.site.register(Request,RequestAdmin)
# Register your models here.
