from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from users.models import User

# Custom form for creating a new user
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text="Required")
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, help_text="Select your role")

    class Meta(UserCreationForm.Meta):       # The model that this form is based on
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
            "role",
        )            # Fields to include in the form

# Custom form for changing user details
class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User         # The model that this form is based on
        fields = ("email", "first_name", "last_name", "role", "is_active", "is_staff")
