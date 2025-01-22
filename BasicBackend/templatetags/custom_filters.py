from django import template

register = template.Library()


@register.filter
def filter_attendance(attendances, status):
    return [attendance for attendance in attendances if attendance.status == status]


@register.filter
def filter_user_group(group, class_id):
    return group[class_id]


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
