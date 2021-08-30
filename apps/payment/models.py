from django.db import models

# Create your models here.

from omnilatam.apps.utils.models import BaseModel
from omnilatam.apps.user.models import User

class Payment(BaseModel):

	user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
	amount = models.FloatField()

	def __str__(self):
		return self.user.username