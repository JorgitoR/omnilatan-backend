from django.shortcuts import render


from django.views.generic import View 
from django.core.exceptions import ObjectDoesNotExist

# Models
from .models import Payment
from omnilatam.apps.order.models import Order 

# Messages
from django.contrib import messages 

class PaymentView(View):
	def get(self, *args, **kwargs):
		try:
			order = Order.objects.get(user=self.request.user, purchased=False)

			context = {
				'order':order
			}
			return render(self.request, 'payment/payment.html', context)
		except ObjectDoesNotExist:
			return redirect("/")

	def post(self, *args, **kwargs):
		orde =  Order.objects.get(user=self.request.user, purchased=False)
		form = PaymentForm(self.request.POST)
		user = User.obj.get(user=self.request.user)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.user = self.request.user 
			instance.save()
			order = order.update(purchased=True)
			order.save()
			messages.info(request, "Your order was successful!")
			return redirect('')
	
		messages.warning(self.request, "Invalid data received")
		return redirect('')