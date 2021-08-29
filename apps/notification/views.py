
# Decorators
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.views.generic import ListView

# Models
from .models import notificacion

class NotificacionList(ListView):
	model = notificacion
	template_name = 'notificacion/lista.html'
	context_object_name ='notificacion'

	@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):
		return super(NotificacionList, self).dispatch(request, *args, **kwargs)

class Notificaciones(NotificacionList):
	"""
		Pagina index para usuarios autenticados.
	"""

	def get_queryset(self):
		qs = self.request.user.notification.all()
		return qs 