"""Invitations tests."""

# Django
from django.test import TestCase


# Model
from omnilatam.apps.product.models import Category, Product
from omnilatam.apps.order.models import OrderProduct

# Auth
from django.contrib.auth import get_user_model

import random

User = get_user_model() # User.objects.all()

class OrderManagerTestCase(TestCase):

	def create_category(self):
		items = []
		self.categorie_count = random.randint(10, 500)
		for i in range(0, self.categorie_count):
			items.append(Category(name=f'category_{i}'))
		Category.objects.bulk_create(items)
		self.category = Category.objects.all()

	def create_users(self):
		items = []
		self.user_count = random.randint(10, 500)
		for i in range(0, self.user_count):
			items.append(User(username=f'user_{i}', email=f'useremail{i}@gmail.com'))
		User.objects.bulk_create(items)
		self.users = User.objects.all()
    
	def create_product(self):
		items = []
		self.product_count = random.randint(10, 500)
		for i in range(0, self.product_count):
			user_obj = self.users.order_by("?").first()
			category = self.category.order_by("?").first()
			items.append(
				Product(
					user = user_obj,
					title=f'products id {i}', 
					category=category,

				)
			)

		Product.objects.bulk_create(items)
		self.products = Product.objects.all()


	def create_orderproduct(self):
		items = []
		self.orderproduct_totals = []
		self.orderproduct_count = 1_000
		for i in range(0, self.orderproduct_count):
			user_obj = self.users.order_by("?").first()
			product_obj = self.products.order_by("?").first()
			items.append(
				OrderProduct(
					user=user_obj,
					content_object=product_obj,
                 
				)
			)
		OrderProduct.objects.bulk_create(items)
		self.orderproduct = OrderProduct.objects.all()

	def setUp(self):
		"""Test case setup."""
		self.create_category()
		self.create_users()
		self.create_product()
		self.create_orderproduct()

	def test_user_count(self):
		qs = User.objects.all()
		self.assertTrue(qs.exists())
		self.assertEqual(qs.count(), self.user_count)
		self.assertEqual(self.users.count(), self.user_count)

	def test_product_count(self):
		qs = Product.objects.all()
		self.assertTrue(qs.exists())
		self.assertEqual(qs.count(), self.product_count)
		self.assertEqual(self.products.count(), self.product_count)

	def test_orderproduct_count(self):
		qs = OrderProduct.objects.all()
		self.assertTrue(qs.exists())
		self.assertEqual(qs.count(), self.orderproduct_count)
		self.assertEqual(self.orderproduct.count(), self.orderproduct_count)
