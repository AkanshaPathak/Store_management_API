from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from users import views as user_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("register/", include("users.urls", namespace="users")),
    path("login/", auth_views.LoginView.as_view(template_name="users/login.html"), name="login"),
    path("logout/",auth_views.LogoutView.as_view(template_name="users/logout.html"),name="logout"),
    path("users", include("users.urls", namespace="users")),
    path("categories/", include("categories.urls", namespace="category")),
    path("products/", include("products.urls", namespace="products")),
    path("", user_views.HomeView.as_view(), name="home"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
