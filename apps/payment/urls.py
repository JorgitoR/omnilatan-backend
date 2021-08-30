from django.urls import path 

from .views import PaymentView

urlpatterns = [
	
	path('payment/order/', PaymentView.as_view(), name='payment')
]