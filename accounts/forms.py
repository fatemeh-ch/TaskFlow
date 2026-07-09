from accounts.models import User
from django.contrib.auth.forms import UserCreationForm


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
