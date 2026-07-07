from django.db import models
from core.models import TimeStampedModel
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils.translation import gettext_lazy as _

# Create your models here.


class CustomUserManager(UserManager):
    """
        Custom manager for the User model.

        Provides helper methods for creating regular users and superusers
        using email as the unique authentication field.
    """

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_("Email must be set"))

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True'))

        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True'))

        return self.create_user(email=email, password=password, **extra_fields)


class User(AbstractUser, TimeStampedModel):
    """
        Custom user model that uses email as the unique identifier
        instead of username for authentication.
    """
    objects = CustomUserManager()
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150, blank=True)
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
