from django.db import models
from django.conf import settings
from categories.models import Category
from django.core.exceptions import ValidationError



class Product(models.Model):
    STATUS_CHOICES = (
        ('available', 'Available'),
        ('unavailable', 'Unavailable'),
    )

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='products_created')
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='products_updated')
    video = models.FileField(upload_to='videos/', null=True, blank=True)
    # isko uncomment karna h akku ko

    
    def save(self, *args, **kwargs):
        # Check if the price is positive
        if self.price <= 0:
            raise ValidationError("The price must be positive")
        # Automatically set the created_by and updated_by fields
        if not self.pk:
            # If the product is new, set the created_by field
            self.created_by = kwargs.pop('user', None)
        self.updated_by = kwargs.pop('user', None)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
