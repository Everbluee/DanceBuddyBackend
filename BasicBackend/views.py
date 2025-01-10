import json
from itertools import groupby

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

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


@login_required
@user_passes_test(is_instructor)
def save_dance_class_attendance(request, class_id):
    if request.method == "POST":
        dance_class = get_object_or_404(DanceClass, id=class_id)

        if dance_class.instructor != request.user:
            return JsonResponse({'error': 'Unauthorized'}, status=403)

        for key, value in request.POST.items():
            if key.startswith("attendances-"):
                user_id = key.split("-")[1]
                try:
                    user = User.objects.get(id=user_id)
                    attendance, created = DanceClassAttendance.objects.get_or_create(user=user, dance_class=dance_class)
                    attendance.status = value
                    attendance.save()
                except User.DoesNotExist:
                    continue

        messages.success(request, "Attendance successfully saved!")
        return redirect('manage_dance_classes')

    return JsonResponse({'error': 'Invalid request'}, status=400)


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

    return render(request, 'manage_dance_classes.html', {
        'instructor_classes': instructor_classes,
        'attendances': attendances,
        'grouped_attendances': grouped_attendances,
        'grouped_attendances_js': json.dumps(grouped_attendances_js),
        'grouped_users_js': json.dumps(grouped_users_js)
    })


def manage_events(request):
    return render(request, 'manage_events.html')
