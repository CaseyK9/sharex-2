from django.contrib import admin
from .models import Account


class AccountAdmin(admin.ModelAdmin):
	list_display = ('id', 'email', 'get_role')

	def get_role(self, account):
		return "Driver" if account.is_driver else "Customer"

	get_role.short_description = "Role"

admin.site.register(Account, AccountAdmin)
