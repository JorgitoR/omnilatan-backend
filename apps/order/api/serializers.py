"""Order serializers."""


# Django REST Framework
from rest_framework import serializers

# Models
from omnilatam.apps.order.models import Order, ProductsOrdered, OrderProduct
from omnilatam.apps.product.models import Product

class ProductSerializer(serializers.ModelSerializer):

	class Meta:
		model = Product
		fields = (
			'title',
		)


class OrderProductSerializer(serializers.ModelSerializer):
	
	products = ProductSerializer(read_only=True)

	class Meta:
		model = OrderProduct
		fields = (
			'products'
		)

class ProductsOrderedSerializer(serializers.ModelSerializer):

	order_product = OrderProductSerializer(read_only=True)

	class Meta:
		model = ProductsOrdered
		fields = (
			'order_product',
		)

class OrderSerializer(serializers.ModelSerializer):

	products_ordered = ProductsOrderedSerializer(read_only=True)

	class Meta:
		model = Order 
		fields = (
			'user',
			'purchased',
			'status',
			'products_ordered'
		)
