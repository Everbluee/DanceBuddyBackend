from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from multiselectfield import MultiSelectField


class BaseAttendance(models.Model):
    ATTENDANCE_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
    ]

    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name="%(class)s_attendances",
                             db_constraint=False)
    status = models.CharField(max_length=10, choices=ATTENDANCE_STATUS_CHOICES, default='pending')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.user.username} - {self.get_status_display()}"


class User(AbstractUser):
    image = models.ImageField(upload_to='users/', null=True, blank=True)
    phone_number = models.CharField(max_length=9, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith(('pbkdf2_sha256$', 'bcrypt$', 'argon2')):
            self.password = make_password(self.password)

        super().save(*args, **kwargs)


# CLASS MODELS
class DanceClass(models.Model):
    LEVEL_CHOICES = [
        ('beginner', 'Begginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced')
    ]
    DAY_CHOICES = [
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday')
    ]

    title = models.CharField(max_length=100)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='beginner')
    description = models.TextField()
    time = models.TimeField()
    days = MultiSelectField(choices=DAY_CHOICES)
    users = models.ManyToManyField('User', through='DanceClassAssignment', related_name='dance_classes')
    instructor = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='instructed_classes')

    def __str__(self):
        return f"{self.title} ({self.level})"


class DanceClassAssignment(models.Model):
    dance_class = models.ForeignKey(DanceClass, on_delete=models.CASCADE, related_name='dance_class_assignments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_dance_class_assignments')

    class Meta:
        unique_together = ('dance_class', 'user')

    def __str__(self):
        return f"{self.user.username} assigned to {self.dance_class.title}"


class DanceClassAttendance(BaseAttendance):
    dance_class = models.ForeignKey(DanceClass, on_delete=models.CASCADE, related_name="class_attendances")
    session_date = models.DateField()

    class Meta:
        unique_together = ('user', 'dance_class', 'session_date')

    def __str__(self):
        return f"{self.user.username} - {self.dance_class.title} - {self.session_date} - {self.status}"


# EVENTS MODELS
class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    time = models.TimeField()
    date = models.DateField()
    location = models.TextField(max_length=100)
    image = models.ImageField(upload_to='events/', null=True, blank=True)
    users = models.ManyToManyField('User', through='EventAssignment', related_name='events')

    def __str__(self):
        return self.title


class EventAssignment(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='event_assignments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_event_assignments')

    class Meta:
        unique_together = ('event', 'user')

    def __str__(self):
        return f"{self.user.username} assigned to {self.event.title}"


class EventAttendance(BaseAttendance):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="event_attendances")

    class Meta:
        unique_together = ('user', 'event')

    def __str__(self):
        return f"{self.user.username} - {self.event.title} - {self.status}"
