from django.contrib.auth.models import AbstractUser, Group
from django.db import models


class BaseAttendance(models.Model):
    ATTENDANCE_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
    ]

    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name="%(class)s_attendances", db_constraint=False)
    status = models.CharField(max_length=10, choices=ATTENDANCE_STATUS_CHOICES, default='pending')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.user.username} - {self.get_status_display()}"


class DanceClass(models.Model):
    LEVEL_CHOICES = [
        ('beginner', 'Begginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]

    title = models.CharField(max_length=100)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='beginner')
    description = models.TextField()
    time = models.TimeField()
    days = models.TextField(max_length=100)  # Example: Monday, Tuesday
    users = models.ManyToManyField('User', through='ClassAttendance', related_name='dance_classes')
    instructor = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, blank=True, related_name='instructed_classes')

    def __str__(self):
        return f"{self.title} ({self.level})"


class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    time = models.TimeField()
    date = models.DateField()
    location = models.TextField(max_length=100)
    image = models.ImageField(upload_to='events/', null=True, blank=True)
    users = models.ManyToManyField('User', through='EventAttendance', related_name='events')

    def __str__(self):
        return self.title


class User(AbstractUser):
    image = models.ImageField(upload_to='users/', null=True, blank=True)
    phone_number = models.CharField(max_length=9, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class ClassAttendance(BaseAttendance):
    dance_class = models.ForeignKey(DanceClass, on_delete=models.CASCADE, related_name="class_attendances")

    class Meta:
        unique_together = ('user', 'dance_class')

    def __str__(self):
        return f"{self.user.username} - {self.dance_class.title} - {self.status}"


class EventAttendance(BaseAttendance):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="event_attendances")

    class Meta:
        unique_together = ('user', 'event')

    def __str__(self):
        return f"{self.user.username} - {self.event.title} - {self.status}"
