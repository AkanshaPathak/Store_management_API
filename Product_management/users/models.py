from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.utils import timezone

# Custom manager for the User model
class CustomUserManager(BaseUserManager):
    # Method to create a regular user
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)             # Normalize the email address
        user = self.model(email=email, **extra_fields)   # Create a user instance
        user.set_password(password)
        user.save(using=self._db)                         # Save the user to the database
        return user
     
    # Method to create a superuser
    def create_superuser(self, email, password=None, **extra_fields):
        # Ensure default values for superuser fields
        extra_fields.setdefault("is_staff", True)   # Superuser must be a staff member
        extra_fields.setdefault("is_superuser", True) # Superuser must have superuser privileges
        extra_fields.setdefault("role", User.ADMIN)   # Default role for superuser is Admin
# Validate that the superuser has the required fields set to True
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        if extra_fields.get("role") is not User.ADMIN:
            raise ValueError("Superuser must have role=Admin.")
# Create and return the superuser with the validated fields
        return self.create_user(email, password, **extra_fields)

# Custom user model
class User(AbstractBaseUser, PermissionsMixin):
    ADMIN = 1
    STAFF = 2
    USER = 3
    ROLE_CHOICES = (
        (ADMIN, "Admin"),
        (STAFF, "Staff"),
        (USER, "User"),
    )

    email = models.EmailField(unique=True)  # Email field with unique constraint
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    # role = models.CharField(max_length=1, choices=ROLE_CHOICES, default=USER)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, default=USER)

    objects = CustomUserManager()           # Assign the custom manager

    USERNAME_FIELD = "email"       # Use email as the unique identifier for authentication
    REQUIRED_FIELDS = []           # No additional fields are required

    def __str__(self):
        return self.email          # String representation of the user, returns the email
