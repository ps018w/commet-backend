from django.contrib import admin

# Register your models here.

from .models import CustomUser,Calendar,DayOfWeek

#admin.site.register(CustomUser)
#admin.site.register(Calendar)
admin.site.register(DayOfWeek)


@admin.register(CustomUser)
class CalendarAdmin(admin.ModelAdmin):

    fieldsets = (
        (
            None,
            {
                "fields":(
                    "email",
                    "full_name",
                    "time_zone",
                    "is_active",
                    "is_staff",
                    "user_type",
                )
            },
        ),

        #("important dates", {"fields":("start_time", "modified_at")})
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
                "fields":(
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

        #("important dates", {"fields":("start_time", "modified_at")})
    )
    list_display = (
        "user",
        "schedule_date",
        "days_of_week",
        "start_time"
    )
