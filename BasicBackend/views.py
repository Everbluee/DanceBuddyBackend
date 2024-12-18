from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
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
def manage_dance_class_attendance(request, class_id):
    dance_class = get_object_or_404(DanceClass, id=class_id)
    attendances = DanceClassAttendance.objects.filter(dance_class=dance_class)
    return render(request, 'manage_dance_attendance.html', {'attendances': attendances})


@login_required
@user_passes_test(is_instructor)
def manage_event_attendance(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    event_attendances = EventAttendance.objects.filter(event=event)
    return render(request, 'manage_event_attendance.html', {'event_attendances': event_attendances})


@login_required
@user_passes_test(is_instructor)
def mark_dance_class_attendance(request, class_id, user_id, status):
    dance_class = get_object_or_404(DanceClass, id=class_id)
    user = get_object_or_404(User, id=user_id)

    valid_statuses = ['pending', 'present', 'absent', 'late']
    if status not in valid_statuses:
        return JsonResponse({'error': 'Invalid status'}, status=400)

    attendance, created = DanceClassAttendance.objects.get_or_create(user=user, dance_class=dance_class)
    attendance.status = status
    attendance.save()

    return JsonResponse({'message': f'Attendance updated to {status} for {user.username} in Dance Class'})


@login_required
@user_passes_test(is_instructor)
def mark_event_attendance(request, event_id, user_id, status):
    event = get_object_or_404(Event, id=event_id)
    user = get_object_or_404(User, id=user_id)

    valid_statuses = ['pending', 'present', 'absent', 'late']
    if status not in valid_statuses:
        return JsonResponse({'error': 'Invalid status'}, status=400)

    event_attendance, created = EventAttendance.objects.get_or_create(user=user, event=event)
    event_attendance.status = status
    event_attendance.save()

    return JsonResponse({'message': f'Attendance updated to {status} for {user.username} in Event'})


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
