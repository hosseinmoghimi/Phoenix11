from django.apps import AppConfig


APP_NAME = 'polls'
class SampleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'polls'
