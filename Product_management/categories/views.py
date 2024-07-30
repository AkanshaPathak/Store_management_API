from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Category
from .forms import CategoryForm

class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'categories/category_list.html'
    context_object_name = 'categories'

class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'categories/category_form.html'
    success_url = '/categories/'  # Redirect URL after successful form submission

class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'categories/category_form.html'
    success_url = '/categories/'

class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = 'categories/category_confirm_delete.html'
    success_url = '/categories/'








# from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required
# from .models import Category
# from .forms import CategoryForm

# @login_required
# def category_list(request):
#     categories = Category.objects.all()
#     return render(request, 'categories/category_list.html', {'categories': categories})

# @login_required
# def category_create(request):
#     if request.method == 'POST':
#         form = CategoryForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('category_list')
#     else:
#         form = CategoryForm()
#     return render(request, 'categories/category_form.html', {'form': form})

# @login_required
# def category_update(request, pk):
#     category = Category.objects.get(pk=pk)
#     if request.method == 'POST':
#         form = CategoryForm(request.POST, instance=category)
#         if form.is_valid():
#             form.save()
#             return redirect('category_list')
#     else:
#         form = CategoryForm(instance=category)
#     return render(request, 'categories/category_form.html', {'form': form})

# @login_required
# def category_delete(request, pk):
#     category = Category.objects.get(pk=pk)
#     if request.method == 'POST':
#         category.delete()
#         return redirect('category_list')
#     return render(request, 'categories/category_confirm_delete.html', {'category': category})
