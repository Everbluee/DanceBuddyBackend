from django import template

register = template.Library()


@register.filter
def filter_attendance(attendances, status):
    return [attendance for attendance in attendances if attendance.status == status]
