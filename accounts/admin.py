from django.contrib import admin

# Register your models here.

from .models import CustomUser,Calendar,RecurrencePattern,DayOfWeek

admin.site.register(CustomUser)
admin.site.register(Calendar)
admin.site.register(RecurrencePattern)
admin.site.register(DayOfWeek)
