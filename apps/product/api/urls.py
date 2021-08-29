from django.urls import path, include


from .views import ProductViewSet, ProductListAPIView

# Django REST Framework
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'product', ProductViewSet, basename='users')


urlpatterns = [
	
	path('', include(router.urls)),
	path('list/product/', ProductListAPIView.as_view(), name='product_list')

]