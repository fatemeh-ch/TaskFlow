from django.shortcuts import render
from django.views.generic import RedirectView
from django.urls import reverse_lazy

# Create your views here.

class HomeRedirectView(RedirectView):

    permanent = False

    def get_redirect_url(self, *args, **kwargs):

        if self.request.user.is_authenticated:
            return reverse_lazy("tasks:dashboard")

        return reverse_lazy("accounts:login")

