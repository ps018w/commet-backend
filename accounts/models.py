
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from .constant import TIMEZONES, USER_TYPES, DAY_OF_WEEK, FREQUENCY_CHOICES
from django.db import models
from multiselectfield import MultiSelectField


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=50, blank=True)
    time_zone = models.CharField(max_length=100, blank=True, null=True, choices=TIMEZONES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    user_type = models.CharField(max_length=100, blank=True, null=True, choices=USER_TYPES)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return self.email



class DayOfWeek(models.Model):
    name = models.CharField(max_length=9,choices=DAY_OF_WEEK)

    def __str__(self):
        return self.name

class Calendar(models.Model):
    user= models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=False)
    description = models.TextField(blank=True)

    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES, default='Monthly',null=True, blank=True)

    days_of_week =models.CharField(null=True, blank=True,max_length=300, choices=DAY_OF_WEEK)# models.ManyToManyField(DayOfWeek, blank=True)

    start_time = models.TimeField(blank=True, null=True,)
    schedule_date = models.DateField(blank=True, null=True)
    start_date = models.DateField(blank=True,null=True)
    end_date = models.DateField(blank=True,null=True)

    def __str__(self):
        return f"{self.title} - {self.start_time}"


