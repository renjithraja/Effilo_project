from django.db import models
from django.contrib.auth.models import AbstractUser,User

class UserProfile(AbstractUser):
    # Add any additional fields you need here
    age = models.PositiveIntegerField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)  # Nullable email field
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='user_profiles',  # Custom related name to avoid clashes
        related_query_name='user_profile',
        blank=True,
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='user_profiles',  # Custom related name to avoid clashes
        related_query_name='user_profile',
        blank=True,
        verbose_name='user permissions',
    )

    def __str__(self):
        return self.username

class Product(models.Model):
    STATUS_CHOICES = [
        ('S', 'S'),
        ('M', 'M'),
        ('L', 'L'),
        ('XL', 'XL'),
        ('XXL', 'XXL')
    ]
    Sex_choice = [
        ('M', 'M'),
        ('F', 'F'),
        ('O', 'O')
    ]
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=255, default='')
    material = models.CharField(max_length=255, default='')
    Size = models.CharField(max_length=255, choices=STATUS_CHOICES, default='M')  # Default to 'M'
    Sex = models.CharField(max_length=255, choices=Sex_choice, default='M')  # Default to 'M'
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='productimages/')
    is_active = models.BooleanField(default=True)
    quantity = models.IntegerField(default=0)
    reorderlevel = models.IntegerField(default=0)

    def is_at_reorder_level(self):
        return self.quantity == self.reorderlevel

    def __str__(self):
        return self.name

    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Cart for {self.user.username}: {self.product.name}"
    

class Order(models.Model):
    STATUS_CHOICES = [
        ('processing', 'Processing'),
        ('out_for_delivery', 'Out for Delivery'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=False)
    fullname = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=10)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='processing')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order for {self.fullname} placed on {self.created_at}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in order {self.order.id}"