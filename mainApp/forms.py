"""
forms.py

This module defines the forms used in the application. These forms handle user authentication, registration,
profile updates, vehicle management, and reviews. Each form is designed to interact with the corresponding
models and provide a user-friendly interface for data input.

Classes:
    LoginForm: Handles user login with username and password fields.
    SignUpForm: Handles user registration with additional user type selection (Customer, Owner, Admin).
    UserUpdateForm: Handles updating user email.
    ProfileUpdateForm: Handles updating user profile details like full name, profile picture, and phone number.
    VehicleForm: Handles adding or updating vehicle details.
    ReviewForm: Handles submitting reviews for vehicles.
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Vehicles, Review, Profile


USER_TYPE_CHOICES = [
    (0, 'Customer'),
    (1, 'Owner'),
    (2, 'Admin'),
]


class LoginForm(forms.Form):
    """
    Form for user login.

    Attributes:
        username (CharField): Input field for the username.
        password (CharField): Input field for the password, rendered as a password input.
    """

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )


class SignUpForm(UserCreationForm):
    """
    Form for user registration.

    Attributes:
        username (CharField): Input field for the username.
        password1 (CharField): Input field for the password, rendered as a password input.
        password2 (CharField): Input field for confirming the password, rendered as a password input.
        email (CharField): Input field for the email address.
        user_type (TypedChoiceField): Dropdown field for selecting the user type (Customer, Owner, Admin).

    Methods:
        save: Overrides the save method to set user roles based on the selected user type.
    """

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    email = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )

    user_type = forms.TypedChoiceField(
        label="Register As",
        choices=USER_TYPE_CHOICES,
        coerce=int,
        widget=forms.Select(
            attrs={
                "class": "form-control"
            }
        )
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        """
        Saves the user instance and sets the user role based on the selected user type.

        Args:
            commit (bool): If True, the user instance is saved to the database.

        Returns:
            User: The saved user instance.
        """
        user = super().save(commit=False)
        user_type = self.cleaned_data['user_type']
        if user_type == 2:
            user.is_admin = True
            user.is_owner = False
            user.is_customer = False
        elif user_type == 1:
            user.is_admin = False
            user.is_owner = True
            user.is_customer = False
        else:
            user.is_admin = False
            user.is_owner = False
            user.is_customer = True
        if commit:
            user.save()
        return user


class UserUpdateForm(forms.ModelForm):
    """
    Form for updating user email.

    Attributes:
        email (EmailField): Input field for the email address.
    """

    class Meta:
        model = User
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control custom-email-class'}),
        }


class ProfileUpdateForm(forms.ModelForm):
    """
    Form for updating user profile details.

    Attributes:
        full_name (CharField): Input field for the user's full name.
        profile_picture (FileField): Input field for uploading a profile picture.
        phone_number (CharField): Input field for the user's phone number.
    """

    class Meta:
        model = Profile
        fields = ['full_name', 'profile_picture', 'phone_number']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control custom-full-name-class'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control custom-profile-picture-class'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control custom-phone-number-class'}),
        }


class VehicleForm(forms.ModelForm):
    """
    Form for adding or updating vehicle details.

    Attributes:
        vehicle_model (CharField): Input field for the vehicle model.
        rent_price (IntegerField): Input field for the rental price.
        category (ModelChoiceField): Dropdown field for selecting the vehicle category.
        description (CharField): Input field for the vehicle description.
        image (ImageField): Input field for uploading a vehicle image.
    """

    class Meta:
        model = Vehicles
        fields = ['vehicle_model', 'rent_price', 'category', 'description', 'image']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
        }


class ReviewForm(forms.ModelForm):
    """
    Form for submitting reviews for vehicles.

    Attributes:
        rating (ChoiceField): Dropdown field for selecting a rating (1 to 5).
        comment (TextField): Input field for the review comment.
    """

    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(choices=[(i, i) for i in range(1, 6)], attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }
