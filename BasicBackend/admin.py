from django.contrib import admin

from .models import User, DanceClass, DanceClassAttendance, EventAttendance, Event, DanceClassAssignment

# Register your models here
admin.site.register(User)
admin.site.register(DanceClass)
admin.site.register(Event)
admin.site.register(DanceClassAttendance)
admin.site.register(EventAttendance)
admin.site.register(DanceClassAssignment)
