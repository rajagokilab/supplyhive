from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta

# -------------------------------
# CATEGORY & PRODUCT
# -------------------------------
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='products', null=True, blank=True
    )
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    bulk_price_info = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    rating = models.PositiveSmallIntegerField(default=5)
    description = models.TextField(blank=True)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


# -------------------------------
# CONTACT MESSAGES
# -------------------------------
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"


# -------------------------------
# ORDER & ORDER ITEMS
# -------------------------------
class Order(models.Model):
    PAYMENT_CHOICES = (
        ('credit_card', 'Credit Card'),
        ('paypal', 'PayPal'),
        ('cod', 'Cash on Delivery'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)  # must be logged-in
    created_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_mode = models.CharField(max_length=50, choices=PAYMENT_CHOICES)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Order {self.id} - {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # price per item

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    @property
    def total_price(self):
        return self.price * self.quantity

    @property
    def delivery_date(self):
        return self.order.created_at + timedelta(days=7)


# -------------------------------
# CART
# -------------------------------
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    @property
    def total_price(self):
        return self.product.price * self.quantity
