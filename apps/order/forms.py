from django import forms 

PURCHASE_STATUS = (
    ('sent', 'Sent'),
)

class OrderSendForm(forms.Form):
	status = forms.ChoiceField(choices=PURCHASE_STATUS)
