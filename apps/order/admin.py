"""Order models Admin."""

# Django
from django.contrib import admin

# Models
from .models import (OrderProduct, Order, ProductsOrdered)



admin.site.register(OrderProduct)
admin.site.register(Order)
admin.site.register(ProductsOrdered)