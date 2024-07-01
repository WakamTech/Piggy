from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
import random
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import AbstractUser, BaseUserManager
import random
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission

import random
from django.utils import timezone
from datetime import timedelta



import uuid

class CustomUserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError('The Phone number must be set')
        username = str(uuid.uuid4())  # Génère un identifiant unique
        user = self.model(phone=phone, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(phone, password, **extra_fields)

class User(AbstractUser):
    ROLE_CHOICES = [
        ('farmer', 'Fermier'),
        ('buyer', 'Acheteur'),
        ('butcher', 'Boucherie'),
        ('admin', 'Administrateur'),
    ]

    phone = models.CharField(max_length=15, unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    address = models.CharField(max_length=255, blank=True, null=True)
    notifications = models.BooleanField(default=True)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    groups = models.ManyToManyField(
        Group,
        related_name='marketplace_user_set',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='marketplace_user_permissions_set',
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='user',
    )

    objects = CustomUserManager()

    def __str__(self):
        return self.phone

class Ad(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    quantity = models.IntegerField()
    price_per_kg = models.DecimalField(max_digits=10, decimal_places=2)
    weight_avg = models.DecimalField(max_digits=10, decimal_places=2)
    race = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    images = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class Location(models.Model):
    ad = models.OneToOneField(Ad, on_delete=models.CASCADE, related_name='location')
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    address = models.CharField(max_length=255)

    def __str__(self):
        return f"Location for {self.ad.title}"

class DeliveryFee(models.Model):
    zone_name = models.CharField(max_length=255)
    base_fee = models.DecimalField(max_digits=10, decimal_places=2)
    fee_per_km = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.zone_name

class Butchery(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('accepted', 'Acceptée'),
        ('rejected', 'Rejetée'),
        ('delivered', 'Livrée'),
        ('cancelled', 'Annulée'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    address = models.CharField(max_length=255)
    payment_method = models.CharField(max_length=50)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Review(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review {self.rating} by {self.user.username}"

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    items = models.JSONField(default=list)

    def __str__(self):
        return f"Cart for {self.user.username}"


class OTP(models.Model):
    phone = models.CharField(max_length=15)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        return self.created_at >= timezone.now() - timedelta(minutes=5)

    @staticmethod
    def generate_code():
        return str(random.randint(100000, 999999))

class Config(models.Model):
    key = models.CharField(max_length=255, unique=True)
    value = models.TextField()

    def __str__(self):
        return self.key
