from django.shortcuts import render

# Models
from omnilatam.apps.order.models import Order

def signup(request):
	return render(request, 'user/signup.html')


def login(request):
	return render(request, 'user/login.html')


def profile(request):

	orders = Order.objects.filter(product__order_product__user=request.user).distinct()

	context = {
		'orders':orders
	}
	return render(request, 'user/profile.html', context)