"""Profile model."""

# Django
from django.db import models

# Utilities
from omnilatam.apps.utils.models import BaseModel

class Profile(BaseModel):
	"""Profile models.

	A profile holds a user's public data like biography, picture,
	and statistics.
	"""

	user = models.OneToOneField('user.User', on_delete=models.CASCADE)

	picture = models.ImageField(
		'profile picture',
		upload_to='users/picture',
		blank=True,
		null=True
	)
	biography = models.TextField(max_length=225, blank=True)

	
	def __str__(self):
		return str(self.user)