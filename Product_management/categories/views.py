from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from categories.models import Category
from categories.forms import CategoryForm

# ListView to display all categories
class CategoryListView(LoginRequiredMixin, ListView):
    model = Category                                 # category app Model to use for this view
    template_name = "categories/category_list.html"   #Template to render the view
    context_object_name = "categories"              # Context variable name in the template
    
    def get_queryset(self):
        # Ensure that all users can only view the list of categories
        return Category.objects.all()      #return all categories

# CreateView to create a new category
class CategoryCreateView(LoginRequiredMixin, CreateView): 
    model = Category                                # category Model to use for this view
    form_class = CategoryForm                       # Form class to use for creating a category
    template_name = "categories/category_form.html" # Template to render the view
    success_url = "/categories/"                    # Redirect URL after successful form submission


# UpdateView to update an existing category
class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm                       # Form class to use for updating a category
    template_name = "categories/category_form.html"
    success_url = "/categories/"                     # Redirect URL after successful form submission

# DeleteView to delete an existing category
class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = "categories/category_confirm_delete.html"   # Template to render the view
    success_url = "/categories/"                        # Redirect URL after successful deletion