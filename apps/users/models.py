from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Default custom user model for Django SaaS Boilerplate.
    For adding more fields later.
    """
    email = models.EmailField(_("email address"), unique=True)

    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(_("bio"), blank=True, null=True)

    stripe_customer_id = models.CharField(max_length=100, blank=True, null=True)
    stripe_subscription_id = models.CharField(max_length=100, blank=True, null=True)

    is_pro_member = models.BooleanField(default=False)

    terms_agreed = models.BooleanField(default=False)


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email
