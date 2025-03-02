"""
urls.py

This module defines the URL patterns for the application. It maps URLs to their corresponding views,
enabling navigation and functionality across the application. The URLs are organized into sections
for profiles, dashboards, payments, reviews, categories, authentication, and password reset.

URL Patterns:
    - Home and About: Basic pages like homepage and about page.
    - Profiles: URLs for customer, owner, and admin profiles.
    - Dashboards: URLs for customer and owner dashboards, including vehicle rental and management.
    - Payments: URLs for Khalti payment integration.
    - Reviews and Ratings: URLs for vehicle reviews and ratings.
    - Categories: URLs for viewing all categories, individual categories, and vehicles.
    - Access Denial: URLs for access denial pages.
    - Authentication: URLs for user login, registration, and logout.
    - Password Reset: URLs for password reset functionality.
"""

from django.urls import path, include
from mainApp.views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Home and About
    path('', homepage, name='home'),
    path('about/', about_page, name='about'),

    # Profiles
    path('customer_details/', customer_details, name='customer_details'),
    path('owner_details/', owner_details, name='owner_details'),
    path('admin_home/', admin_home, name='admin_home'),

    # Dashboards
    # Customer Dashboard
    path('rent_page/<int:id>', rent_page, name='rent_page'),
    path('renting/', renting, name='renting'),

    # Khalti Payment Integration
    path('initiate/', initkhalti, name="initiate"),
    path('verify/', verifyKhalti, name="verify"),

    # Owner Dashboard
    path('vehicle_on_rent/', vehicle_on_rent, name='vehicle_on_rent'),
    path('on_leash/', on_leash, name='on_leash'),
    path('returned_leash/<int:id>', returned_leash, name='returned_leash'),
    path('vehicle/update/<int:id>/', vehicle_update, name='vehicle_update'),
    path('vehicle_register/', vehicle_register, name='vehicle_register'),
    path('delete/<int:id>', vehicle_delete, name='vehicle_delete'),

    # Reviews and Ratings
    # (Add specific URLs for reviews and ratings if needed)

    # Categories
    path('category/', category_all, name='all_category'),
    path('vehicle/<int:id>', vehicle, name='vehicle'),
    path('individual_category/<str:space>', category_individual, name='individual_category'),
    path('all_vehicles/', all_vehicles, name='all_vehicles'),
    path('search_vehicle/', search_vehicle, name='search_vehicle'),

    # Access Denial
    path('auth_denied/', auth_denied, name='auth_denied'),
    path('customer_needed/', customer_needed, name='customer_needed'),

    # Authentication
    path('login/', login_view, name='login_view'),
    path('register/', register, name='register'),
    path('logout/', log_out, name='logout'),

    # Password Reset
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='auth/password_reset.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='auth/password_reset_done.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='auth/password_confirm.html'), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='auth/password_reset_complete.html'), name='password_reset_complete'),
]