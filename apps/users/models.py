from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser, BaseUserManager


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save User with the give email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extrafields):
        """
        Create and save a Superuser with the given email and password.
        """
        extrafields.setdefault('is_staff', True)
        extrafields.setdefault('is_superuser', True)
        extrafields.setdefault('is_active', True)

        if extrafields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extrafields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extrafields)


class User(AbstractUser):
    """
    Default custom user model for Django SaaS Boilerplate.
    For adding more fields later.
    """
    username = models.CharField(
        max_length=150,
        unique=True,
        blank=True,
        null=True
    )
    email = models.EmailField(_("email address"), unique=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(_("bio"), blank=True, null=True)
    stripe_customer_id = models.CharField(max_length=100, blank=True, null=True)
    stripe_subscription_id = models.CharField(max_length=100, blank=True, null=True)
    is_pro_member = models.BooleanField(default=False)
    terms_agreed = models.BooleanField(default=False)


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
