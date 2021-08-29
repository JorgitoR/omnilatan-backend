from django.urls import path 

from .views import  add_to_cart, SumaryOrder, remove_single_product, OrderSeller

urlpatterns = [

	path('summary/order/', SumaryOrder.as_view(), name='order-sumary'),
	path('add_cart/<slug>/', add_to_cart, name='add_to_cart'),
	path('remove_single_to_cart/<slug>/', remove_single_product, name='remove_single_to_cart'),

	path('order-seller/<pk_order>/', OrderSeller, name='order-seller'),
]