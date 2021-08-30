from django import forms

# Models
from .models import Payment 

class PaymentForm(forms.ModelForm):

	class Meta():
		model = Payment
		fields = ['amount']