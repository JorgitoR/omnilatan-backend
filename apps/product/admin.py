"""Order models Admin."""

# Django
from django.contrib import admin

# Models
from .models import (Category, Product, ProductRelated)

class ProductRelatedInline(admin.TabularInline):
	model = ProductRelated
	fk_name ='item'
	extra = 0

class ProductAdmin(admin.ModelAdmin):
	inline = [ProductRelatedInline]
	class Meta:
		model = Product 



admin.site.register(Category)
admin.site.register(Product, ProductAdmin)