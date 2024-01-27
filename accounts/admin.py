from django.contrib import admin

# Register your models here.

from .models import CustomUser, Calendar, DayOfWeek, UserDetails, Timeslot, BookingSlot, TeachingClass, UserEducation, \
    TeachingPreference, Subjects, SubjectSpecialization, MediaGallery

# admin.site.register(CustomUser)
# admin.site.register(Calendar)
admin.site.register(DayOfWeek)
admin.site.register(UserDetails)
admin.site.register(Timeslot)
admin.site.register(TeachingClass)
admin.site.register(UserEducation)
admin.site.register(TeachingPreference)
admin.site.register(Subjects)
admin.site.register(SubjectSpecialization)
admin.site.register(MediaGallery)
admin.site.register(BookingSlot)


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "full_name",
                    "time_zone",
                    "is_active",
                    "is_staff",
                    "user_type",
                    "password"
                )
            },
        ),

        # ("important dates", {"fields":("start_time", "modified_at")})
    )
    list_display = (
        "email",
        "user_type",
    )


@admin.register(Calendar)
class CalendarAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "user",
                    "title",
                    "description",
                    "frequency",
                    "days_of_week",
                    "start_time",
                    "schedule_date",
                    "start_date",
                    "end_date",
                )
            },
        ),

        # ("important dates", {"fields":("start_time", "modified_at")})
    )
    list_display = (
        "user",
        "schedule_date",
        # "days_of_week",
        "start_time"
    )
