from django.shortcuts import render, redirect
from django.urls import reverse_lazy
# from Product_management import categories
from .models import Product, Category
from django.views.generic import FormView,ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .utils import encrypt_data, decrypt_data
from .forms import DummyDataForm
from django.views import View
from categories.models import Category
from django.http import HttpResponse
import random
import csv

class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        user = self.request.user
        if user.role == 'Admin':
            return Product.objects.all()
        elif user.role == 'Staff':
            return Product.objects.filter(created_by=user)
            # return Product.objects.filter(status__in=['Pending', 'Approved'])
        else: #user role 
            # return Product.objects.filter(updated_by=user)
            return Product.objects.all()
        
        
class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    fields = ['category', 'title', 'description', 'price', 'status', 'video']
    template_name = 'products/product_form.html'
    success_url = reverse_lazy('products:product_list')  # Redirects to product list after successful creation
    
    def form_valid(self, form):
         # Automatically associate the current user with the product
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'
    

class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    fields = ['category', 'title', 'description', 'price', 'status', 'video']
    template_name = 'products/product_form.html'
    success_url = reverse_lazy('products:product_list')

    def form_valid(self, form):
        # Encrypt sensitive data before saving
        form.instance.description = encrypt_data(form.cleaned_data['description'])
        # form.instance.updated_by = self.request.user
        return super().form_valid(form)

    # def form_valid(self, form):
    #     form.instance.updated_by = self.request.user
    #     return super().form_valid(form)

    def test_func(self):
        # Ensure only admins or staff can update
        return self.request.user.role in ['Admin', 'Staff']

class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'products/product_confirm_delete.html'
    success_url = reverse_lazy('products:product_list')

    def test_func(self):
        # Ensure only admins can delete
        return self.request.user.role == 'Admin'
    
class ExportProductsCSVView(View):
    """
    A view to export the list of products as a CSV file.
    """

    def get(self, request, *args, **kwargs):
        # Create a response object and set the content type to 'text/csv'
        response = HttpResponse(content_type='text/csv')
        # Specify the Content-Disposition header to prompt a file download
        response['Content-Disposition'] = 'attachment; filename="products.csv"'

        # Create a CSV writer object to write data to the response
        writer = csv.writer(response)
        # Write the header row to the CSV file
        writer.writerow(['ID', 'Title', 'Category', 'Description', 'Price', 'Status'])

        # Query the Product model for all products and extract the necessary fields
        products = Product.objects.all().values_list('id', 'title', 'category__name', 'description', 'price', 'status')
        # Iterate over the products and write each one to the CSV file
        for product in products:
            writer.writerow(product)

        # Return the response, which will prompt the browser to download the file
        return response


class CreateDummyProductsView(View):
    def get(self, request):
        return render(request, 'products/generate_dummy.html')
    
    def post(self, request):
        product_count = int(request.POST.get('product_count', 0))
        categories = Category.objects.all()

        if categories.exists():
            for _ in range(product_count):
                category = random.choice(categories)
                Product.objects.create(
                    category=category,
                    title=f"Product {_ + 1}",
                    description="This is a dummy product description.",
                    price=random.uniform(10.0, 1000.0),
                    status="available",
                )
            message = f"{product_count} dummy products created successfully."
        else:
            message = "No categories found. Please create some categories first."

        return render(request, 'products/generate_dummy.html', {'message': message})


