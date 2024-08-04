from django.urls import path
from users.views import RegisterView, HomeView, activate
from django.contrib.auth.views import LoginView, LogoutView

app_name = "users"

urlpatterns = [
    path("login/", LoginView.as_view(template_name="users/login.html"), name="login"),
    path(
        "register/",
        RegisterView.as_view(template_name="users/register.html"),
        name="register",
    ),
    path("", HomeView.as_view(), name="home"),
    path(
        "logout/", LogoutView.as_view(template_name="users/logout.html"), name="logout"
    ),
    path("activate/<uidb64>/<token>/", activate, name="activate"),
]
