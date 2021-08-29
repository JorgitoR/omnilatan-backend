"""User model."""

# Django
from django.db import models
from django.contrib.auth.models import AbstractUser

# Utilities
from omnilatam.apps.utils.models import BaseModel

class User(BaseModel, AbstractUser):
	"""User Model.

	Extend from Django's Abstract User.
	"""
	email = models.EmailField(
		'email address',
		unique=True,
		error_messages={
			'unique':'A user with that email already exists.'
		}
	)

	is_seller = models.BooleanField(
		'seller',
		default=False,
		help_text='Set to true if the person sells something'
	)

	is_customer = models.BooleanField(
		'customer',
		default=False,
		help_text='Set to True if the person just buy'
	)

	is_verified = models.BooleanField(
		'verified',
		default=True,
		help_text='Set to true when the user have verified its email address.'
	)

	

	def __str__(self):
		"""Return username."""
		return self.username 

	def get_shor_name(self):
		"""Return Username."""
		return self.username