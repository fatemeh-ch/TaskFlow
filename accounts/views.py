from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import FormView
from django.contrib.auth import login

from accounts.forms import SignupForm , LoginForm

# Create your views here.


class CustomLoginView(LoginView):
    """
        Authenticate existing users.

        Displays the login form and signs users in using Django's
        authentication system. Authenticated users are redirected
        away from the login page automatically.
    """

    template_name = 'accounts/login.html'
    authentication_form = LoginForm
    # redirect_authenticated_user = True


class CustomLogoutView(LogoutView):
    """
        Log the current user out.

        Ends the user's authenticated session and redirects
        them back to the login page.
    """

    next_page = reverse_lazy('accounts:login')


class SignupView(FormView):
    """
        Register a new user.

        Creates a new account using the signup form, immediately
        authenticates the user after successful registration,
        and redirects them to the main dashboard.
    """

    form_class = SignupForm
    template_name = 'accounts/signup.html'
    # success_url = reverse_lazy('tasks:dashboard')

    def form_valid(self, form):
        """
            Save the new user and log them in automatically.

            Once the signup form is successfully validated, the user
            account is created, an authenticated session is started,
            and the standard success redirect is returned.
        """
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)
