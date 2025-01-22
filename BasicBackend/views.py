import json
from datetime import date
from itertools import groupby

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .forms import DanceClassAttendanceForm, DanceClassForm, AddParticipantsForm
from .serializers import *


@api_view(['GET'])
def get_data_dance_class(request):
    items = DanceClass.objects.all()
    serializer = DanceClassSerializer(items, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def create_data_dance_class(request):
    serializer = DanceClassSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_data_dance_class(request, pk):
    DanceClass.objects.filter(pk=pk).delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['DELETE'])
def delete_all_data_dance_class(request):
    DanceClass.objects.all().delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['PATCH'])
def update_data_dance_class(request, pk):
    try:
        dance_class = DanceClass.objects.get(pk=pk)
    except DanceClass.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = DanceClassSerializer(dance_class, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_data_event(request):
    items = Event.objects.all()
    serializer = EventSerializer(items, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def create_data_event(request):
    serializer = EventSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_data_event(request, pk):
    Event.objects.filter(pk=pk).delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['DELETE'])
def delete_all_data_event(request):
    Event.objects.all().delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['PATCH'])
def update_data_event(request, pk):
    try:
        event = Event.objects.get(pk=pk)
    except Event.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = EventSerializer(event, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_all_data_user(request):
    users = get_user_model().objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_data_user(request, pk):
    try:
        user = get_user_model().objects.get(pk=pk)
    except get_user_model().DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = UserSerializer(user)

    return Response(serializer.data)


@api_view(['POST'])
def create_data_user(request):
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_data_user(request, pk):
    get_user_model().objects.filter(pk=pk).delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['DELETE'])
def delete_all_data_event(request):
    get_user_model().objects.all().delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['PATCH'])
def update_data_user(request, pk):
    try:
        user = get_user_model().objects.get(pk=pk)
    except get_user_model().DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = UserSerializer(user, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def is_instructor(user):
    return user.groups.filter(name='Instructor').exists()


def home(request):
    is_user_instructor = is_instructor(request.user)
    return render(request, 'home.html', {'is_instructor': is_user_instructor})


@login_required
def dashboard(request):
    is_user_instructor = is_instructor(request.user)

    if is_user_instructor:
        return render(request, 'instructor_dashboard.html')
    else:
        return render(request, 'user_dashboard.html')


@login_required
@user_passes_test(is_instructor)
def manage_dance_classes(request):
    instructor_classes = DanceClass.objects.filter(instructor=request.user)
    attendances = DanceClassAttendance.objects.filter(dance_class__in=instructor_classes).order_by(
        'dance_class', 'session_date'
    )
    status_choices = [
        ('pending', 'Pending'),
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
    ]

    grouped_attendances = {}
    for dance_class, class_group in groupby(attendances, key=lambda x: x.dance_class):
        grouped_attendances[dance_class] = {}
        for session_date, date_group in groupby(class_group, key=lambda x: x.session_date):
            grouped_attendances[dance_class][session_date] = list(date_group)

    grouped_attendances_js = {}
    for dance_class, class_group in groupby(attendances, key=lambda x: x.dance_class):
        grouped_attendances_js[dance_class.id] = {}
        for session_date, date_group in groupby(class_group, key=lambda x: x.session_date):
            session_date_str = session_date.strftime('%Y-%m-%d')
            grouped_attendances_js[dance_class.id][session_date_str] = [
                {'status': attendance.status, 'user': attendance.user.id}
                for attendance in date_group
            ]

    grouped_users_js = {}
    for dance_class in instructor_classes:
        grouped_users_js[dance_class.id] = [
            {'first_name': user.first_name, 'last_name': user.last_name, 'id': user.id}
            for user in dance_class.users.all()
        ]

    grouped_users = {}
    for dance_class in instructor_classes:
        grouped_users[dance_class.id] = [
            {'first_name': user.first_name, 'last_name': user.last_name, 'id': user.id}
            for user in dance_class.users.all()
        ]

    return render(request, 'manage_dance_classes.html', {
        'instructor_classes': instructor_classes,
        'attendances': attendances,
        'status_choices': status_choices,
        'users': User.objects.filter(groups__name='Dancer'),
        'instructors': User.objects.filter(groups__name='Instructor'),
        'dance_classes': DanceClass.objects.filter(instructor=request.user),
        'grouped_attendances': grouped_attendances,
        'grouped_attendances_js': json.dumps(grouped_attendances_js),
        'grouped_users': grouped_users,
        'grouped_users_js': json.dumps(grouped_users_js),
        'today_date': date.today().strftime('%Y-%m-%d'),
    })


@login_required
@user_passes_test(is_instructor)
def create_attendance(request, dance_class_id):
    dance_class = DanceClass.objects.get(pk=dance_class_id)

    if request.method == 'POST':
        form = DanceClassAttendanceForm(request.POST, dance_class_id=dance_class_id)
        form.dance_class = dance_class

        if form.is_valid():
            form.save()
            messages.success(request, "Attendance created successfully.")
        else:
            messages.error(request, "There was an error with the form. Please try again.")

    return redirect(request.META.get('HTTP_REFERER', 'manage_dance_classes'))


@login_required
@user_passes_test(is_instructor)
def create_dance_class(request):
    if request.method == 'POST':
        form = DanceClassForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Dance class created successfully.")
        else:
            messages.error(request, "There was an error with the form. Please try again.")

    return redirect(request.META.get('HTTP_REFERER', 'manage_dance_classes'))


@login_required
@user_passes_test(is_instructor)
def add_participant(request, dance_class_id):
    dance_class = DanceClass.objects.get(pk=dance_class_id)

    if request.method == 'POST':
        form = AddParticipantsForm(request.POST, instance=dance_class)
        if form.is_valid():
            form.save()
            messages.success(request, "Participants created successfully.")
    else:
        messages.error(request, "There was an error with the form. Please try again.")

    return redirect(request.META.get('HTTP_REFERER', 'manage_dance_classes'))


@login_required
@user_passes_test(is_instructor)
def manage_events(request):
    return render(request, 'manage_events.html')
