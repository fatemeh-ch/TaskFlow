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
        """
            Create a user with the given password and email
        """

        if not email:
            raise ValueError(_("Email must be set"))

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
            Create and save a superuser with the given password and email
        """

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


class Profile(TimeStampedModel, models.Model):
    """
    Stores additional information associated with a user account,
    including avatar and biography.
    """

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(
        blank=True, upload_to='accounts/avatars/')
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.email} Profile"
