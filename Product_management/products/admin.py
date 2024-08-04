from django.contrib import admin
from products.models import Product
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "category",
        "price",
        "status",
        "created_by",
        "updated_by",
        "created_at",
        "updated_at",
    )
    list_filter = ("status", "category", "created_by", "updated_by")
    search_fields = ("title", "description")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.role == User.ADMIN:
            return qs  # Admin sees all products
        elif request.user.role == User.STAFF:
            return qs.filter(
                created_by=request.user
            )  # Staff sees only products they created
        else:
            return qs.filter(status="Approved")  # End User sees only approved products

    def has_add_permission(self, request):
        if request.user.role in [User.ADMIN, User.STAFF]:
            return True
        return False

    def has_change_permission(self, request, obj=None):
        if request.user.role == User.ADMIN:
            return True
        elif (
            request.user.role == User.STAFF and obj is not None and obj.created_by == request.user):
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.role == User.ADMIN:
            return True
        return False


admin.site.register(Product, ProductAdmin)
