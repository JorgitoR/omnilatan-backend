"""User models admin."""

# Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Models
from omnilatam.apps.user.models import User, Profile


class CustomUserAdmin(UserAdmin):
	"""User model admin."""

	list_display = ('email', 'username', 'first_name', 'is_seller', 'is_customer')
	list_filter = ('is_seller', 'is_customer', 'created', 'modified')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
	"""Profile model Admin."""

	list_display = ('user',)

admin.site.register(User, CustomUserAdmin)