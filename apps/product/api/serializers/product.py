"""Product serializers."""

# Django REST Framework
from rest_framework import serializers

# Models 
from omnilatam.apps.product.models import Product


class ProductModelSerializer(serializers.ModelSerializer):

	user = serializers.HiddenField(default=serializers.CurrentUserDefault())


	class Meta:

		model = Product
		fields = ('user', 'category', 'title', 'imagen', 'description', 'stock', 'price', 'slug')
