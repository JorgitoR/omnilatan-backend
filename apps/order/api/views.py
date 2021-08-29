"""Order api Views."""

# Django REST Fremework
from rest_framework import mixins, status, viewsets, generics
from rest_framework.decorators import action 
from rest_framework.response import Response

from omnilatam.apps.order.api.serializers import OrderSerializer, ProductsOrderedSerializer

# Models
from omnilatam.apps.order.models import Order, ProductsOrdered, OrderProduct
from omnilatam.apps.product.models import Product



class OrderViewSet(mixins.RetrieveModelMixin,
				  mixins.UpdateModelMixin,
				  viewsets.GenericViewSet):

	serializer_class=OrderSerializer

	def get_queryset(self, *args, **kwargs):
		order_id = self.kwargs.get("pk")
		order = Order.objects.get(pk=order_id)
		product_order = ProductsOrdered.objects.filter(order=order, product__order_product__user=self.request.user)
		
		return product_order

	def product(self, request, *args, **kwargs):
		order = self.get_object()
		

	def retrieve(self, request, *args, **kwargs):
		response = super(OrderViewSet, self).retrieve(request, *args, **kwargs)
		order_id = self.kwargs.get("pk")
		order = Order.objects.get(pk=order_id)
		product_order = ProductsOrdered.objects.filter(order=order, product__order_product__user=request.user)

		data = {
			'order': order,
		}
		return Response(data, status=status.HTTP_200_OK)