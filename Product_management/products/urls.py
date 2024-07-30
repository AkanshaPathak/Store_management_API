from django.urls import path
from .views import (
    ProductListView,
    ProductCreateView,
    ProductDetailView,
    ProductUpdateView,
    ProductDeleteView,
    CreateDummyProductsView,
    ExportProductsCSVView,
)

app_name = 'products'  

urlpatterns = [
    path('list/', ProductListView.as_view(), name='product_list'),
    path('create/', ProductCreateView.as_view(), name='product_create'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('generate-dummy/', CreateDummyProductsView.as_view(), name='generate_dummy'),
    path('export/csv/', ExportProductsCSVView.as_view(), name='export_products_csv'),
]
