from django.test import TestCase

from django.utils import timezone
from django.utils.text import slugify


# Models
from omnilatam.apps.product.models import Category, Product

# Auth
from django.contrib.auth import get_user_model


User = get_user_model() # User.objects.all()

class MovieProxyTestCase(TestCase):

	def create_user(self):
		user_a = User.objects.create(username='jorgito', email='jorgito@gmail.com')
		self.user_a = user_a

	def create_category(self):
		category_a = Category.objects.create(name='Technologie')
		category_b = Category.objects.create(name='Fitness')
		category_c = Category.objects.create(name='Apple')
		self.category_a = category_a
		self.category_b = category_b
		self.category_c = category_c

	def create_product(self):
		product_a = Product.objects.create(user=self.user_a, title='My title', category=self.category_a)
		product_b = Product.objects.create(user=self.user_a, title='My title',  category=self.category_b)
		product_c = Product.objects.create(user=self.user_a, title='My title',  category=self.category_c)
		self.product_a = product_a
		self.product_b = product_b
		self.product_c = product_c
		self.product_qs = Product.objects.all()

	def setUp(self):
		self.create_user()
		self.create_category()
		self.create_product()
   
	def test_category_product(self):
		categorya_a = self.category_a
		product_a = self.product_a.category
		self.assertEqual(categorya_a, product_a)

	def test_product_items(self):
		count = self.product_qs.count()
		self.assertEqual(count, 3)

   
        