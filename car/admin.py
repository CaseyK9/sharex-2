from django.contrib import admin
from .models import Car

class CarAdmin(admin.ModelAdmin):
	list_display = ('id','get_email','license')

	def get_email(self,car):
		return car.account.email if car.account else ""

	get_email.short_description = "Email"
admin.site.register(Car,CarAdmin)
# Register your models here.
