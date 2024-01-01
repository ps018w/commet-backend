from django.contrib import admin

# Register your models here.

from .models import CustomUser,Calendar,DayOfWeek

admin.site.register(CustomUser)
admin.site.register(Calendar)
admin.site.register(DayOfWeek)
