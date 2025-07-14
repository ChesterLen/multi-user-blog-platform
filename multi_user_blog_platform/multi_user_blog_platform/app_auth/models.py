from django.db import models
from django.contrib.auth import models as auth_models
from django.contrib.auth.hashers import make_password
from datetime import datetime


class AppUserManager(auth_models.BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class AppUser(auth_models.PermissionsMixin, auth_models.AbstractBaseUser):
    email = models.EmailField(unique=True, null=False, blank=False)
    date_joined = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    objects = AppUserManager()

    USERNAME_FIELD = 'email'


class Pet(models.Model):
    name = models.CharField(max_length=300, null=False, blank=False)
    description = models.TextField(max_length=500, default='Hello there', null=True, blank=True)
    age = models.IntegerField(default=0, null=False, blank=False)
    breed = models.CharField(max_length=300, null=True, blank=False)

    user = models.OneToOneField(to=AppUser, on_delete=models.CASCADE)