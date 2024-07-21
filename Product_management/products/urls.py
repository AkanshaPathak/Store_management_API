# products/urls.py

from django.urls import path
from .views import ProductListCreateView, CategoryListCreateView

urlpatterns = [
    path('products/', ProductListCreateView.as_view(), name='product-list'),
    path('categories/', CategoryListCreateView.as_view(), name='category-list'),
]
