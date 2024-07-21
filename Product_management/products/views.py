# products/views.py

from django.shortcuts import render
from django.views.generic import ListView
from products.models import Product, Category

class ProductListCreateView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'

class CategoryListCreateView(ListView):
    model = Category
    template_name = 'products/category_list.html'
    context_object_name = 'categories'

