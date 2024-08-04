from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from products.models import Product
from categories.models import Category
from users.models import User
from django.views.generic import (
    View,
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from products.utils import encrypt_data, decrypt_data
from products.forms import DummyDataForm
from django.views import View
from categories.models import Category
from django.http import HttpResponse
import random
import csv

# ListView to display all products
class ProductListView(LoginRequiredMixin, ListView):
    model = Product                                 # Product Model to use for this view
    template_name = "products/product_list.html"     # Template to render the view
    context_object_name = "products"                 # Context variable name in the template

    def get_queryset(self):            
        user = self.request.user          # Get the current logged-in user
        if user.role == User.ADMIN:
            return Product.objects.all()  # Admin can see all products
        elif user.role == User.STAFF:
            return Product.objects.all()  # Staff can see all products
            # return Product.objects.filter(created_by=user)
        else:  # User role
            return Product.objects.filter(status="available")    # Users can see only available products

# CreateView to create a new product
class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    fields = ["category", "title", "description", "price", "status", "video"]   # Fields to include in the form
    template_name = "products/product_form.html"
    success_url = reverse_lazy("products:product_list")  # Redirects to product list after successful creation

    def form_valid(self, form):
        user = self.request.user     # Get the current logged-in user
        if user.role in [User.ADMIN, User.STAFF]:
            form.instance.created_by = user    # Set the created_by field to the current user
            return super().form_valid(form)    # Call the superclass form_valid method
        else:
            return self.form_invalid(form)      # If user is not admin or staff, invalidate the form

# DetailView to display a single product's details
class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = "products/product_detail.html"
    context_object_name = "product"             # Context variable name in the template

# UpdateView to update an existing product
class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    fields = ["category", "title", "description", "price", "status", "video"]      # Fields to include in the form
    template_name = "products/product_form.html"
    success_url = reverse_lazy("products:product_list")
    
    
    def form_valid(self, form):
        user = self.request.user                # Get the current logged-in user
        if user.role in [User.ADMIN, User.STAFF]:
            form.instance.updated_by = user      # Set the updated_by field to the current user
            return super().form_valid(form)      # Call the superclass form_valid method
        else:
            return self.form_invalid(form)       # If user is not admin or staff, invalidate the form

# DeleteView to delete an existing product
class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = "products/product_confirm_delete.html"       # Template to render the view
    success_url = reverse_lazy("products:product_list")

    def test_func(self):
        # Ensure only admins can delete
        return self.request.user.role == User.ADMIN

# View to export the list of products as a CSV file
class ExportProductsCSVView(View):

    def get(self, request, *args, **kwargs):
        # Create a response object and set the content type to 'text/csv'
        response = HttpResponse(content_type="text/csv")
        # Specify the Content-Disposition header to prompt a file download
        response["Content-Disposition"] = 'attachment; filename="products.csv"'

        # Create a CSV writer object to write data to the response
        writer = csv.writer(response)
        # Write the header row to the CSV file
        writer.writerow(["ID", "Title", "Category", "Description", "Price", "Status"])

        # Query the Product model for all products and extract the necessary fields
        products = Product.objects.all().values_list(
            "id", "title", "category__name", "description", "price", "status"
        )
        # Iterate over the products and write each one to the CSV file
        for product in products:
            writer.writerow(product)

        # Return the response, which will prompt the browser to download the file
        return response

# View to create dummy products
class CreateDummyProductsView(View):
    def get(self, request):
        return render(request, "products/generate_dummy.html")   # Render the dummy product generation form

    def post(self, request):
        # Get the number of dummy products to create
        product_count = int(request.POST.get("product_count", 0))
        categories = Category.objects.all()             # Get all categories

        if categories.exists():
            for _ in range(product_count):
                category = random.choice(categories)      # Randomly choose a category for each dummy product
                Product.objects.create(
                    category=category,
                    title=f"Product {_ + 1}",             # Set the title of the dummy product with a unique number
                    description="This is a dummy product description.",
                    price=random.uniform(10.0, 1000.0),   # Set the price of the dummy product to a random value between 10.0 and 1000.0
                    status="available",
                )
            message = f"{product_count} dummy products created successfully."       # Success message
        else:
            message = "No categories found. Please create some categories first."     # Error message if no categories exist

        return render(request, "products/generate_dummy.html", {"message": message})  # Render the form with the message
