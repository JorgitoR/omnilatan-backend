"""Test notification."""

from django.test import TestCase
import pytz 

# Models 
from .models import notificacion

# Signals
from .signals import notify

# Uilities
from django.utils import timezone  
from django.utils.timezone import localtime, utc 

# Settings
from django.conf import settings
from django.test import override_settings


from django.contrib.auth.models import User

class NotificationTest(TestCase):
	'''Django notification automated tests.'''
	@override_settings(USE_TZ=True)
	@override_settings(TIME_ZONE='America/Bogota')
	def test_use_timezone(self):
		actor = User.objects.create(username='actor', password='pwd', email='actor@gmail.com')
		receiver = User.objects.create(username='receiver', password='pwd', email='receiver@gmail.com')
		notify.send(actor, actor=actor, receiver=receiver, verb='text')
		notification = notificacion.objects.get(receiver=receiver)
		date = (
			timezone.now().replace(tzinfo=utc) - localtime(notification.timestamp, pytz.timezone(settings.TIME_ZONE))
		)
		self.assertTrue(date.seconds < 60)