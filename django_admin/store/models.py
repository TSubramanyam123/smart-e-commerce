from django.db import models


class Category(models.Model):

    id = models.BigAutoField(
        primary_key=True
    )

    name = models.CharField(
        max_length=100,
        unique=True
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    class Meta:

        managed = False

        db_table = "categories"

    def __str__(self):

        return self.name


class Product(models.Model):

    id = models.BigAutoField(
        primary_key=True
    )

    category = models.ForeignKey(
        Category,
        db_column="category_id",
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING
    )

    name = models.CharField(
        max_length=200
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    price = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    stock = models.IntegerField(
        default=0
    )

    image_url = models.URLField(
        blank=True,
        null=True
    )

    is_active = models.BooleanField(
        default=True
    )

    popularity = models.IntegerField(
        default=0
    )

    created_at = models.DateTimeField()

    class Meta:

        managed = False

        db_table = "products"

    def __str__(self):

        return self.name


class Customer(models.Model):

    id = models.BigAutoField(
        primary_key=True
    )

    name = models.CharField(
        max_length=120
    )

    email = models.EmailField(
        unique=True
    )

    password_hash = models.CharField(
        max_length=255,
        null=True
    )

    role = models.CharField(
        max_length=20
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField()

    class Meta:

        managed = False

        db_table = "users"

    def __str__(self):

        return self.email


class Order(models.Model):

    id = models.BigAutoField(
        primary_key=True
    )

    customer = models.ForeignKey(
        Customer,
        db_column="user_id",
        on_delete=models.DO_NOTHING
    )

    total = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    payment_status = models.CharField(
        max_length=30
    )

    order_status = models.CharField(
        max_length=30
    )

    created_at = models.DateTimeField()

    class Meta:

        managed = False

        db_table = "orders"


class OrderItem(models.Model):

    id = models.BigAutoField(
        primary_key=True
    )

    order = models.ForeignKey(
        Order,
        db_column="order_id",
        related_name="items",
        on_delete=models.DO_NOTHING
    )

    product = models.ForeignKey(
        Product,
        db_column="product_id",
        on_delete=models.DO_NOTHING
    )

    quantity = models.PositiveIntegerField()

    unit_price = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    class Meta:

        managed = False

        db_table = "order_items"


class Payment(models.Model):

    id = models.BigAutoField(
        primary_key=True
    )

    order = models.ForeignKey(
        Order,
        db_column="order_id",
        on_delete=models.DO_NOTHING
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    payment_method = models.CharField(
        max_length=50
    )

    transaction_id = models.CharField(
        max_length=255,
        unique=True,
        null=True
    )

    status = models.CharField(
        max_length=30
    )

    created_at = models.DateTimeField()

    class Meta:

        managed = False

        db_table = "payments"


class Notification(models.Model):

    id = models.BigAutoField(
        primary_key=True
    )

    user = models.ForeignKey(
        Customer,
        db_column="user_id",
        on_delete=models.DO_NOTHING
    )

    type = models.CharField(
        max_length=50
    )

    message = models.TextField()

    is_read = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField()

    class Meta:

        managed = False

        db_table = "notifications"
