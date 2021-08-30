"""Product models."""

# Django
from django.db import models

# Utilities
from omnilatam.apps.utils.models import BaseModel
from django.utils.html import mark_safe, escape
from django.utils.text import slugify

# Models
from omnilatam.apps.user.models import User
from omnilatam.apps.order.models import OrderProduct

# ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType 

# Signals
from django.db.models.signals import post_save

class Category(BaseModel):
	"""Category models.
	we'll category the products eg. products for house,
	for health care..
	
	"""
	name = models.CharField(
		max_length=20
	)
	color = models.CharField(
		max_length=7, default='#06C503'
	)


	def __str__(self):
		return self.name

	def get_badge(self):
		"""
			This return a tag to renderizer in a html
		"""
		name = escape(self.name)
		color = escape(self.color)
		html = '<button style="background:%s"> %s </>' %(self.color, self.name)
		return mark_safe(html)

class Product(BaseModel):
	"""Produc models.
		Handle the products for the e-commerce, this model allows 
		to create a product
	"""
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product')
	category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='product')
	title = models.CharField(max_length=100)
	imagen = models.ImageField(upload_to='img/product')
	description = models.TextField()

	stock = models.IntegerField(blank=True, null=True)
	price = models.FloatField(blank=True, null=True)

	order = GenericRelation(OrderProduct, related_query_name='order_product')

	slug = models.SlugField(blank=True, null=True, unique=True)

	parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.SET_NULL)
	relateds = models.ManyToManyField('self', blank=True, related_name='relacion', through='ProductRelated',  symmetrical=False)


	def __str__(self):
		"""Return title."""
		return self.title

	@property
	def get_content_type(self):

		content_type = ContentType.objects.get_for_model(Product)
		return content_type

def url(instance, new_url=None):
	slug = slugify(instance.title)
	if new_url is not None:
		slug = new_url
	return slug

def slug_save(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = url(instance)

post_save.connect(slug_save, sender=Product)

class ProductRelated(BaseModel):
	item = models.ForeignKey(Product, on_delete=models.CASCADE)
	related = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="item_related")