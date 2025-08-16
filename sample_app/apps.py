from django.apps import AppConfig


APP_NAME = 'sample_app'
class SampleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sample_app'
