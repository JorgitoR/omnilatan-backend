from django.shortcuts import render, redirect


from django.views.generic import View 
from django.core.exceptions import ObjectDoesNotExist

# Models
from .models import Payment
from omnilatam.apps.order.models import Order 

# Forms
from .forms import PaymentForm

# Messages
from django.contrib import messages 


# signals
from omnilatam.apps.notification.signals import notify

class PaymentView(View):
	def get(self, *args, **kwargs):
		try:
			order = Order.objects.get(user=self.request.user, purchased=False)

			context = {
				'order':order,
				'form':PaymentForm()
			}
			return render(self.request, 'payment/payment.html', context)
		except ObjectDoesNotExist:
			return redirect("/")

	def post(self, *args, **kwargs):
		order =  Order.objects.get(user=self.request.user, purchased=False)
		form = PaymentForm(self.request.POST)

		if form.is_valid():
			instance = form.save(commit=False)
			instance.user = self.request.user 
			instance.save()
			order.purchased=True
			order.payment = instance
			verb = "statu of the order: {} Completed successful!".format(order.id)
			notify.send(self.request.user , actor=self.request.user, receiver=self.request.user, verb=verb)
			order.save()
			messages.info(self.request, "Your order was successful!")
			return redirect('/')
	
		messages.warning(self.request, "Invalid data received")
		return redirect('/')