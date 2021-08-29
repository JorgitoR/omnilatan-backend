from django.urls import path

from .views import Notificaciones

urlpatterns = [
	
	path('notify/', Notificaciones.as_view(), name='notificaciones')
]