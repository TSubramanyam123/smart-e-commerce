from django.contrib import admin

from .models import (
    Category,
    Product,
    Customer,
    Order,
    OrderItem,
    Payment,
    Notification
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name"
    )

    search_fields = (
        "name",
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "category",
        "price",
        "stock",
        "is_active",
        "popularity"
    )

    list_filter = (
        "is_active",
        "category"
    )

    search_fields = (
        "name",
        "description"
    )

    list_editable = (
        "price",
        "stock",
        "is_active"
    )


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "email",
        "role",
        "is_active",
        "created_at"
    )

    list_filter = (
        "role",
        "is_active"
    )

    search_fields = (
        "name",
        "email"
    )


class OrderItemInline(
    admin.TabularInline
):

    model = OrderItem

    extra = 0

    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "customer",
        "total",
        "payment_status",
        "order_status",
        "created_at"
    )

    list_filter = (
        "payment_status",
        "order_status"
    )

    search_fields = (
        "customer__email",
    )

    list_editable = (
        "payment_status",
        "order_status"
    )

    inlines = [
        OrderItemInline
    ]


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "order",
        "amount",
        "payment_method",
        "transaction_id",
        "status",
        "created_at"
    )

    list_filter = (
        "status",
        "payment_method"
    )


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "type",
        "is_read",
        "created_at"
    )

    list_filter = (
        "type",
        "is_read"
    )

    search_fields = (
        "message",
        "user__email"
    )

