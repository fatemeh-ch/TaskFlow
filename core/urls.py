from django.urls import path, include

from .views import HomeRedirectView

urlpatterns = [
    path("", HomeRedirectView.as_view(), name="home"),
]