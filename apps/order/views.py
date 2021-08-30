from django.shortcuts import render, redirect, get_object_or_404

# Models
from .models import (OrderProduct, Order, ProductsOrdered)
from omnilatam.apps.product.models import Product

# Views Generics
from django.views.generic import ListView, CreateView

# Utilities
from django.utils import timezone 

from django.db.models import Sum 
from django.contrib import messages 
from django.core.exceptions import ObjectDoesNotExist

from django.views.generic import View 

def OrderSeller(request, pk_order):
	"""Order seller
		This function allows to the user seller or store see the order of 
		the customer
	"""
	order = get_object_or_404(Order, pk=pk_order)
	product_order = ProductsOrdered.objects.filter(order=order, product__order_product__user=request.user)
	
	context = {
		'order':order,
		'products':product_order
	}

	return render(request, 'order/seller.html', context)

class SumaryOrder(View):
	"""Sumary Order
		This  views allow us to render the products ordered
	"""

	def get(self, *args, **kwargs):
		try:
			order = Order.objects.get(user=self.request.user, purchased=False)

			context = {
				'order':order
			}

			return render(self.request, 'order/sumary.html', context)
		except ObjectDoesNotExist:
			messages.warning(self.request, "You dont't have an order still")
			return redirect("/")

def add_to_cart(request, slug):
	"""Add to cart
	This view allows customer to choose item to purchase
	without actually completing the payment.
	"""

	#we take the instance of the product to add
	product = get_object_or_404(Product, slug=slug)

	order_product, created = OrderProduct.objects.get_or_create(
		content_type=product.get_content_type,
		object_id= product.id,
		user=request.user,
		purchased=True 
	)

	order_qs = Order.objects.filter(user=request.user, purchased=False)

	if order_qs.exists():
		order = order_qs[0]

		ordered_quantity =OrderProduct.objects.filter(order_product__slug=product.slug, purchased=True).aggregate(total=Sum('amount'))
		total_order=ordered_quantity['total']
		min_order=1
		if total_order >= min_order:
			available = product.stock - total_order

			if order_product.amount == available or order_product.amount < available:
				if order.product.filter(order_product__slug=product.slug).exists():
					order_product.amount += 1
					order_product.save()
					messages.info(request, "The quantity was update")
					return redirect('order-sumary')
				else:
					order = ProductsOrdered.objects.create(
						product= order_product,
						order=order
					)
					messages.info(request, "This product was added to your cart")
					return redirect('order-sumary')
			else:
				messages.info(request, "Maximum available Quantity")
				return redirect('order-sumary')

	else:
		date = timezone.now()
		order = Order.objects.create(
			user=request.user,

		)

		product_ordered = ProductsOrdered.objects.create(
			product=order_product,
			order=order

		)
		messages.info(request, "This item was added to your cart")
		return redirect('order-sumary')



def remove_single_product(request, slug):
	"""Remove single product

		this function allows to  remove single product
		of the cart
	
	"""
	product = get_object_or_404(Product, slug=slug)

	order_qs = Order.objects.filter(user=request.user, purchased=False)
	if qs.exists():
		order = order_qs[0]

		if order.product.filter(order_product__slug=product.slug).exists():
			order_product = OrderProduct.objects.filter(
				order_product = product,
				user = request.user,
				purchased=True
			)[0]

			if order_product.amount > 0:
				order_product -= 1
				if order_product.amount == 0:
					order_product.delete()
				else:
					order_product.save()

			messages.info(request, "The quantity was update")
			return redirect("order-sumary")

		else:
			messages.info(request, "This product was not in your cart")
			return redirect("detail", slug=slug)
	else:
		messages.info(request,  "You do not have an active order")
		return redirect("detail", slug=slug)