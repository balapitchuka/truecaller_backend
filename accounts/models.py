from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _

# Create your models here.

class UserManager(BaseUserManager):
    """
    Custom user model manager where phone number is the unique identifiers
    for authentication instead of username or email.
    """
    def create_superuser(self, phone_no, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(phone_no, password, **extra_fields)

    def create_user(self, phone_no, password, **extra_fields):
        """
        Create and save a User with the given phone number and password.
        """
        if not phone_no:
            raise ValueError(_('The Email must be set'))
        # email = self.normalize_email(e)
        user = self.model(phone_no=phone_no, **extra_fields)
        user.set_password(password)
        user.save()
        return user

class User(AbstractUser):
    """
    User Model for Registering new users
    """
    username = None
    name = models.CharField(max_length=100)
    phone_no = models.CharField(unique=True, max_length=15)
    email = models.EmailField(null=True, default=None)
    spam = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone_no'
    REQUIRED_FIELDS = ['name']

    objects = UserManager()

    def __str__(self):
        return self.name
