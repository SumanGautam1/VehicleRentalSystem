"""
decorators.py

This module defines custom decorators to restrict access to views based on user roles.
These decorators ensure that only authenticated users with specific roles (admin, owner, or customer)
can access certain views. If the user does not meet the role requirements, they are redirected
to the 'auth_denied' page.

Decorators:
    admin_only: Restricts access to views for admin users only.
    owner_only: Restricts access to views for owner users only.
    customer_only: Restricts access to views for customer users only.
"""

from django.shortcuts import redirect


def admin_only(view_func):
    """
    Decorator to restrict access to views for admin users only.

    Args:
        view_func (function): The view function to be wrapped.

    Returns:
        function: The wrapper function that checks if the user is an admin.
                 If the user is an admin, the view function is called.
                 Otherwise, the user is redirected to the 'auth_denied' page.
    """

    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_admin:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('auth_denied')
    return wrapper_func


def owner_only(view_func):
    """
    Decorator to restrict access to views for owner users only.

    Args:
        view_func (function): The view function to be wrapped.

    Returns:
        function: The wrapper function that checks if the user is an owner.
                 If the user is an owner, the view function is called.
                 Otherwise, the user is redirected to the 'auth_denied' page.
    """

    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_owner:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('auth_denied')
    return wrapper_func


def customer_only(view_func):
    """
    Decorator to restrict access to views for customer users only.

    Args:
        view_func (function): The view function to be wrapped.

    Returns:
        function: The wrapper function that checks if the user is a customer.
                 If the user is a customer, the view function is called.
                 Otherwise, the user is redirected to the 'auth_denied' page.
    """

    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_customer:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('auth_denied')
    return wrapper_func
