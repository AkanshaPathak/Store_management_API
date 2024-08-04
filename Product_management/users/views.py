from email.message import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.views.generic import TemplateView
from users.forms import CustomUserCreationForm
from django.contrib.auth.views import LogoutView
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from .tokens import account_activation_token
from django.contrib.auth import get_user_model
from django.conf import settings
from django.views import View
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
import smtplib

SECRET_KEY = settings.SECRET_KEY


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "home.html"          # Template for the home page


class CustomLogoutView(LogoutView):
    template_name = "users/logout.html"  # Template for the logout page


class RegisterView(View):
    form_class = CustomUserCreationForm
    template_name = "register.html"

    def get(self, request):
        # Display the registration form
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            # Create a new user but set them as inactive until email confirmation
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            
            # Prepare and send the activation email
            current_site = get_current_site(request)
            mail_subject = "Activation link has been sent to your email id"
            message = render_to_string(
                "users/activation_email.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": account_activation_token.make_token(user),
                },
            )
            to_email = form.cleaned_data.get("email")
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            print("email message", EmailMessage)
            return HttpResponse(
                "Please confirm your email address to complete the registration"
            )
        else:
            print("form errors", form.errors)
        return render(request, self.template_name, {"form": form})

# Function to activate user account via email link
def activate(request, uidb64, token):
    User = get_user_model()
    try:
         # Decode the user ID from the URL
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        # Activate the user account and save
        user.is_active = True
        user.save()
        return HttpResponse(
            "Thank you for your email confirmation. Now you can login your account."
        )
    else:
        return HttpResponse("Activation link is invalid!")
