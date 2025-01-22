from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import *

dance_class_patterns = [
    path('', get_data_dance_class, name='get_dance_class'),
    path('create/', create_data_dance_class, name='create_dance_class'),
    path('delete/', delete_all_data_dance_class, name='delete_all_dance_class'),
    path('delete/<int:pk>/', delete_data_dance_class, name='delete_dance_class'),
    path('update/<int:pk>/', update_data_dance_class, name='update_dance_class'),
]

event_patterns = [
    path('', get_data_event, name='get_event'),
    path('create/', create_data_event, name='create_event'),
    path('delete/', delete_all_data_event, name='delete_all_event'),
    path('delete/<int:pk>/', delete_data_event, name='delete_event'),
    path('update/<int:pk>/', update_data_event, name='update_event'),
]

user_patterns = [
    path('', get_all_data_user, name='get_all_user'),
    path('<int:pk>/', get_data_user, name='get_user'),
    path('create/', create_data_user, name='create_user'),
    path('delete/', delete_data_user, name='delete_all_user'),
    path('delete/<int:pk>/', delete_data_user, name='delete_user'),
    path('update/<int:pk>/', update_data_user, name='update_user'),
]

manage_dance_classes_patterns = [
    path('', manage_dance_classes, name='manage_dance_classes'),
    path('create-attendance/<int:dance_class_id>/', create_attendance, name='create_attendance'),
]

management_patterns = [
    path('dance_class/', include(manage_dance_classes_patterns)),
    path('event/', manage_events, name='manage_events'),
]

urlpatterns = [
    path('', home, name='home'),
    path('user/', include('django.contrib.auth.urls')),
                  path('user/login/', auth_views.LoginView.as_view(), name='login'),
    path('user/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('api/dance_class/', include(dance_class_patterns)),
    path('api/event/', include(event_patterns)),
    path('api/user/', include(user_patterns)),
                  path('dashboard/', dashboard, name='dashboard'),
                  path('management/', include(management_patterns)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
