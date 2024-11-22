from django.contrib import admin
from .models import User, DanceClass, ClassAttendance, EventAttendance, Event

# Register your models here
admin.site.register(User)
admin.site.register(DanceClass)
admin.site.register(Event)
admin.site.register(ClassAttendance)
admin.site.register(EventAttendance)

