from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class GeminiApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "gemini_api"
    verbose_name = _("Django Gemini Api")
