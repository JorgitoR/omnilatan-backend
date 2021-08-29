"""Django models utilities."""

# Django
from django.db import models 

class BaseModel(models.Model):

	"""Base Model.

	BaseModel acts as an abstract base class from which every
	other model in the project will inherit. This class provides
	every table with the following attributes:
	 	+ created (DateTime): Store the datetime the object was created.
	 	+ modified (DateTime): Store the last datetime tha object was modified.
	"""

	created = models.DateTimeField(
		'created at',
		auto_now_add=True,
		help_text='Date Time on which the object was created'
	)
	modified = models.DateTimeField(
		'modified at',
		auto_now=True,
		help_text='Date Time on which the object was last modified'
	)

	class Meta:
		"""Meta option."""
		abstract = True
		ordering = ['-created', '-modified']
