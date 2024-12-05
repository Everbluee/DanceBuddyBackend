from django.apps import AppConfig
from django.contrib.auth import get_user_model
from django.db.models.signals import post_migrate


def create_superuser(sender, **kwargs):
    user = get_user_model()
    if not user.objects.filter(username='admin').exists():
        user.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpassword',
            first_name='admin',
            last_name='admin'
        )


class BasicBackendConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'BasicBackend'

    def ready(self):
        post_migrate.connect(create_superuser)
