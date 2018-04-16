from django.contrib import admin
from .models import *
class MatchingAdmin(admin.ModelAdmin):
	list_display = ('id','get_travel_id','get_driver','current_station','status')

	def get_travel_id(self,travel_data):
		return travel_data.pk

	def get_driver(self,travel_data):
		return travel_data.account.email

	get_travel_id.short_description = "travel_id"
	get_driver.short_description = "driver"
admin.site.register(Matching)
# Register your models here.
