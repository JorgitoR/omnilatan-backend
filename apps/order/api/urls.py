from django.urls import path, include

from .views import OrderViewSet


# Django REST Framework
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'order', OrderViewSet, basename='users')


urlpatterns = [
	
	path('', include(router.urls))

]