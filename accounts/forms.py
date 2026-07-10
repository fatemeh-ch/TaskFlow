from accounts.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm


class SignupForm(UserCreationForm):
    """
        Registration form for new users.

        Extends Django's built-in UserCreationForm to work with the
        custom User model. It collects the user's email, first name,
        and password, while handling password confirmation and hashing
        automatically.
    """

    class Meta:
        model = User
        fields = ['email', 'first_name', 'password1', 'password2']
        labels = {
            "email": "ایمیل",
            "first_name": "نام",
            "password1": "رمز عبور",
            "password2": "تکرار رمز عبور",
        }


class LoginForm(AuthenticationForm):

    """
        Authentication form for existing users.

        This form customizes Django's built-in AuthenticationForm by
        providing Persian labels, placeholders, and CSS classes for
        rendering a styled login interface while preserving Django's
        default authentication behavior.
    """

    error_messages = {
        "invalid_login": "ایمیل یا رمز عبور وارد شده صحیح نیست.",
        "inactive": "این حساب کاربری غیرفعال است.",
    }

    username = forms.EmailField(
        label='ایمیل',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'ایمیل خود را وارد کنید',
            'autocomplete': 'email',
        })
    )

    password = forms.CharField(
        label='رمز عبور',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'رمز عبور خود را وارد کنید',
            'autocomplete': 'current-password',
        })
    )
