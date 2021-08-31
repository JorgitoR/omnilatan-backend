"""Product serializers."""

# Django REST Framework
from rest_framework import serializers

# Models 
from omnilatam.apps.product.models import Product, Category

class CategoryModelSerializer(serializers.ModelSerializer):

	class Meta:
		model = Category
		fields = [
			'name'
		]


class ProductModelSerializer(serializers.ModelSerializer):

	user = serializers.HiddenField(default=serializers.CurrentUserDefault())
	category = CategoryModelSerializer(read_only=True)

	class Meta:

		model = Product
		fields = ('user', 'category', 'title', 'imagen', 'description', 'stock', 'price', 'slug')
