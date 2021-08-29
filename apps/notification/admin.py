

from django.contrib import admin

# Models 
from omnilatam.apps.notification.models import notificacion
from omnilatam.apps.notification.utils.admin import AbstractNotificacionAdmin

class NotificacionAdmin(AbstractNotificacionAdmin):
	raw_id_fields = ('receiver', )
	list_display = ('receiver', 'actor', 'verb', 'level', 'read')
	list_filter = ('level', 'read', 'timestamp')

admin.site.register(notificacion, NotificacionAdmin)