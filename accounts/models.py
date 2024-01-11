from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from .constant import TIMEZONES, USER_TYPES, DAY_OF_WEEK, FREQUENCY_CHOICES
from django.db import models
from multiselectfield import MultiSelectField
from phonenumber_field.modelfields import PhoneNumberField


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


class UserDetails(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    hourly_fee = models.IntegerField(blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    zipcode = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=100, blank=True, null=True)
    i_can_teach_on = models.CharField(max_length=100, blank=True, null=True)
    introduction = models.TextField()
    phone_number = PhoneNumberField(blank=True, null=True, region='AU')
    skype_id = models.CharField(max_length=100, blank=True, null=True)
    website = models.CharField(max_length=100, blank=True, null=True)
    whatsapp_number = models.IntegerField()

    def __str__(self):
        return self.user.full_name


class UserEducation(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    degree = models.CharField(max_length=100, blank=True, null=True)
    university = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    current_degree = models.BooleanField(default=False)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.full_name}-{self.degree}"


class Subjects(models.Model):
    subject_name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.subject_name


class SubjectSpecialization(models.Model):
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.subject.subject_name}-{self.specialization}"


class TeachingClass(models.Model):
    class_name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.class_name


class TeachingPreference(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE)
    specialization = models.ManyToManyField(SubjectSpecialization)
    teaching_class = models.ManyToManyField(TeachingClass)

    def __str__(self):
        return self.user.full_name


class MediaGallery(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    file = models.ImageField(upload_to='user_media/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.full_name}-{self.file}"


class DayOfWeek(models.Model):
    name = models.CharField(max_length=9, choices=DAY_OF_WEEK)

    def __str__(self):
        return self.name


class Calendar(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=False)
    description = models.TextField(blank=True)

    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES, default='Monthly', null=True, blank=True)

    days_of_week = models.CharField(null=True, blank=True, max_length=300,
                                    choices=DAY_OF_WEEK)  # models.ManyToManyField(DayOfWeek, blank=True)

    start_time = models.TimeField(blank=True, null=True, )
    schedule_date = models.DateField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} - {self.start_time}"


class Timeslot(models.Model):
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.start_time}-{self.end_time}"


class BookingSlot(models.Model):
    tutor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='tutor_user')
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='student_user')
    approved = models.BooleanField(default=False)
    time_slot = models.ForeignKey(Timeslot, on_delete=models.CASCADE)
    scheduled_calender = models.ForeignKey(Calendar, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.tutor.full_name}-{self.student.full_name}-{self.time_slot}-{self.approved}"
