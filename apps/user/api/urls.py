from django.urls import path, include


from omnilatam.apps.user.api.views import UserViewSet

# Django REST Framework
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')


urlpatterns = [
	
	path('', include(router.urls))

]