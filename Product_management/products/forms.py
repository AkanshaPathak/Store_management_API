from django import forms
from products.models import Product

# Form class for creating and updating Product instances
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product       # The model that this form is based on
        fields = ["category", "title", "description", "price", "status", "video"]

# Form class for generating dummy data
class DummyDataForm(forms.Form):
    category_count = forms.IntegerField(label="Number of Categories")  # Field for the number of categories
    num_products = forms.IntegerField(
        label="Number of Products", min_value=1, initial=1000        # Field for the number of products with a minimum value of 1 and an initial value of 1000
    )
