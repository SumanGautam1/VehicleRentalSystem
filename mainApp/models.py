"""
models.py

This module defines the database models for the application. It includes models for works, categories, users, profiles,
vehicles, rent transactions, and reviews. These models represent the core data structures used in the application.

Classes:
    Works: Represents a work item with a title, image, and description.
    Category: Represents a category for grouping vehicles.
    User: Extends Django's AbstractUser to add custom user roles (admin, customer, owner).
    Profile: Represents a user profile with additional details like profile picture, full name, and phone number.
    Vehicles: Represents a vehicle available for rent, including details like model, price, category, and availability.
    RentTransaction: Represents a transaction record for renting a vehicle.
    Review: Represents a review left by a user for a rented vehicle.
"""

from django.db import models
from django.contrib.auth.models import AbstractUser


class Works(models.Model):
    """
    Represents a work item in the application.

    Attributes:
        title (CharField): The title of the work (max length: 10).
        image (ImageField): An image representing the work, uploaded to 'images/how-it-works'.
        desc (CharField): A short description of the work (max length: 100).
    """

    title = models.CharField(max_length=10)
    image = models.ImageField(upload_to='images/how-it-works')
    desc = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Category(models.Model):
    """
    Represents a category for grouping vehicles.

    Attributes:
        name (CharField): The name of the category (max length: 50).
    """

    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'categories'


class User(AbstractUser):
    """
    Extends Django's built-in AbstractUser to add custom user roles.

    Attributes:
        is_admin (BooleanField): Indicates if the user is an admin (default: False).
        is_customer (BooleanField): Indicates if the user is a customer (default: True).
        is_owner (BooleanField): Indicates if the user is an owner (default: False).
    """

    is_admin = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=True)
    is_owner = models.BooleanField(default=False)


class Profile(models.Model):
    """
    Represents a user profile with additional details.

    Attributes:
        user (OneToOneField): A one-to-one relationship with the User model.
        profile_picture (ImageField): The user's profile picture, uploaded to 'profile_pictures/'.
        full_name (CharField): The user's full name (max length: 20, optional).
        phone_number (CharField): The user's phone number (max length: 10, optional).
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    full_name = models.CharField(max_length=20, blank=True, null=True)
    phone_number = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.user.username


class Vehicles(models.Model):
    """
    Represents a vehicle available for rent.

    Attributes:
        vehicle_model (CharField): The model of the vehicle (max length: 100).
        rent_price (PositiveIntegerField): The rental price of the vehicle (default: 0).
        category (ForeignKey): A foreign key to the Category model.
        description (CharField): A description of the vehicle (max length: 250, optional).
        image (ImageField): An image of the vehicle, uploaded to 'uploads/product/'.
        uploaded_by (ForeignKey): The user who uploaded the vehicle.
        rented_by (ForeignKey): The user who rented the vehicle (optional).
        isDelete (BooleanField): Indicates if the vehicle is marked as deleted (default: False).
        available (BooleanField): Indicates if the vehicle is available for rent (default: True).
    """

    vehicle_model = models.CharField(max_length=100)
    rent_price = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.CharField(max_length=250, default='', blank=True, null=True)
    image = models.ImageField(upload_to='uploads/product/')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_vehicles')
    rented_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='rented_vehicles')
    isDelete = models.BooleanField(default=False)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.vehicle_model


class RentTransaction(models.Model):
    """
    Represents a transaction record for renting a vehicle.

    Attributes:
        vehicle (ForeignKey): A foreign key to the Vehicles model.
        transaction_id (CharField): A unique identifier for the transaction (max length: 100).
        amount (PositiveIntegerField): The amount paid for the rental (default: 0).
        user (ForeignKey): The user who rented the vehicle.
        date_rented (DateTimeField): The date and time when the vehicle was rented (auto-generated).
    """

    vehicle = models.ForeignKey(Vehicles, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=100)
    amount = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_rented = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.transaction_id


class Review(models.Model):
    """
    Represents a review left by a user for a rented vehicle.

    Attributes:
        vehicle (ForeignKey): A foreign key to the Vehicles model.
        user (ForeignKey): A foreign key to the User model.
        rating (PositiveIntegerField): The rating given by the user.
        comment (TextField): The review comment.
        created_at (DateField): The date when the review was created (auto-generated).
    """

    vehicle = models.ForeignKey(Vehicles, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField()
    comment = models.TextField()
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.vehicle.vehicle_model}'
