"""
context_processors.py

This module defines custom context processors for the application. Context processors are functions
that add data to the context of all templates, making it available globally.

Functions:
    all_categories: Adds a list of all categories and the current year to the template context.
"""

from .models import Category
from datetime import datetime


def all_categories(request):
    """
    Context processor to add all categories and the current year to the template context.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        dict: A dictionary containing:
            - 'categories': A queryset of all Category objects.
            - 'current_year': The current year as an integer.
    """
    categories = Category.objects.all()
    current_year = datetime.now().year
    return {'categories': categories, 'current_year': current_year}
