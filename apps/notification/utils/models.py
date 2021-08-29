"""Notification Abstract."""

# Django
from django.db import models

# Models
from omnilatam.apps.user.models import User 
from django.db.models.query import QuerySet

# ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType 

# Utilities
from django.utils import timezone
from swapper import load_model

# Signals
from omnilatam.apps.notification.signals import notify


LEVELS = (
    ('sent', 'Sent'),
    ('received', 'Received'),
)

class NotificacionAbstract(models.Model):
	"""Notificacion Abstract
		
	NotificacionAbstract acts as an abstract base class from which every
	other model in the project will inherit.

	Format:
		<actor> <verb> <date>

		Example:
		<jorgito> <your purchase was sent> <2 minutes ago>

	"""

	level = models.CharField(max_length=20, choices=LEVELS)
	receiver = models.ForeignKey(
		User,
		related_name='notification',
		on_delete=models.CASCADE,
		blank=True,
		null=True
	)
	read = models.BooleanField(default=False, blank=False, db_index=True)

	actor_content_type = models.ForeignKey(ContentType, related_name='actor_notify', on_delete=models.CASCADE)
	actor_object_id = models.PositiveIntegerField()
	actor = GenericForeignKey("actor_content_type", "actor_object_id")

	verb = models.CharField(max_length=225)

	timestamp = models.DateTimeField(default=timezone.now, db_index=True)


	class Meta:
		abstract = True
		ordering = ('-timestamp',)
		index_together = ('receiver', 'read')

	def __str__(self):
		notify = {
			'actor':self.actor,
			'verb': self.verb,
			'date': self.timesince()
		}

		return u"%(actor)s %(verb)s %(date)s" % notify

	def timesince(self, now=None):
		"""
		Shortcut for the django.utils.timesince.timesince function 
		of the current timestamp.
		"""
		from django.utils.timesince import timesince
		return timesince(self.timestamp, now)

	def mark_as_read(self):
		"""Mark read a notify."""
		if self.read:
			self.read = True
			self.save()

	def mark_as_unread(self):
		"""Mark unread a notify."""
		if self.read:
			self.read = False
			self.save()


def notification(verb, **kwargs):
	"""Handler function to create Notification instance upon action signal call."""

	receiver = kwargs.pop('receiver')
	print(receiver)
	actor = kwargs.pop('actor')
	print('Actor', actor)
	level = kwargs.pop('level', LEVELS)
	timestamp = kwargs.pop('timestamp', timezone.now())

	Notify = load_model('notification', 'notificacion')

	# Check if User
	if isinstance(receiver, (QuerySet, list)):
		receivers = receiver
	else:
		receivers = [receiver]

	notifyes = []
	for receiver in receivers:
		newnotify = Notify(
			receiver=receiver,
			actor_content_type=ContentType.objects.get_for_model(actor),
			actor_object_id=actor.pk,
			verb=str(verb),
			timestamp=timestamp,
			level=level
		)

		newnotify.save()
		notifyes.append(newnotify)

	return notifyes

notify.connect(notification, dispatch_uid='notification.models.notificacion')