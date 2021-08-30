"""Order models."""

# Django
from django.db import models

# Utilities
from omnilatam.apps.utils.models import BaseModel


# ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType 

# Models
from omnilatam.apps.user.models import User
from omnilatam.apps.payment.models import Payment

# signals
from omnilatam.apps.notification.signals import notify
from django.db.models.signals import post_save

PURCHASE_STATUS = (
    ('sent', 'Sent'),
    ('received', 'Received'),
)

class OrderProduct(BaseModel):
	"""Order product models.

	"""

	user = models.ForeignKey(User, on_delete=models.CASCADE)
	content_type = models.ForeignKey(
		ContentType,
		verbose_name="models product",
		on_delete=models.CASCADE
	)
	object_id = models.PositiveIntegerField(
		"id of the product"
	)
	content_object = GenericForeignKey("content_type", "object_id")

	purchased = models.BooleanField(default=False)
	amount = models.IntegerField(default=1)

	def __str__(self):
		return self.user.username


class Order(BaseModel):
	"""Order Models.
    1. Item added to cart
    2. Adding a billing address
    (Failed checkout)
    3. Payment
    (Preprocessing, processing, packaging etc.)
    4. Being delivered
    5. Received
    6. Refunds
	"""
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order')
	product = models.ManyToManyField(OrderProduct, through='ProductsOrdered')
	payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
	purchased = models.BooleanField(default=False)
	status = models.CharField(max_length=100, choices=PURCHASE_STATUS)


	def __str__(self):
		"""Return user"""
		return self.user.username


class ProductsOrdered(models.Model):
	product = models.ForeignKey(OrderProduct, on_delete=models.CASCADE)
	order = models.ForeignKey(Order, on_delete=models.CASCADE)


	def __str__(self):
		return "User: {} ordered the next product: {}".format(self.product.content_object.user.username, self.product.content_object.title)

def NotifyOrder(sender, instance, *args, **kwargs):

	verb ="product order: {}".format(instance.product.content_object.title)
	verb_two ="you have ordered the next product: {}".format(instance.product.content_object.title)

	notify.send(instance.product.user, actor=instance.product.user, receiver=instance.product.content_object.user,  verb=verb)
	notify.send(instance.product.user, actor=instance.product.user, receiver=instance.product.user,  verb=verb_two)

post_save.connect(NotifyOrder, sender=ProductsOrdered)
