"""Profile serializer."""

# Django REST Framework
from rest_framework import serializers

# Models
from omnilatam.apps.user.models import Profile

class ProfileModelSerializers(serializers.ModelSerializer):
	"""Profile models serializer."""

	class Meta:
		"""Meta class."""
		model = Profile
		fields = (
			'picture',
			'biography'

		)