from django.db import models
from django.conf import settings
from categories.models import Category
from django.core.exceptions import ValidationError
from users.models import User


class Product(models.Model):
    # Choices for the status field
    STATUS_CHOICES = (
        ("available", "Available"),
        ("unavailable", "Unavailable"),
    )

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)             # Title of the product
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20)              # Status of the product, either 'available' or 'unavailable'
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name="products_created",blank=True)
    updated_by = models.ForeignKey(User, related_name='updated_products', on_delete=models.SET_NULL, null=True, blank=True)
    video = models.FileField(upload_to="videos/", null=True, blank=True)
    
    def __str__(self):
        return self.title      # String representation of the product, returns the title
