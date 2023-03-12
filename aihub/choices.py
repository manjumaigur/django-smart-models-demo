from django.db import models
from django.utils.translation import gettext_lazy as _

# NOTE: Right now, only OpenAPI is supported and more API providers will be added in the future

class APIProviders(models.TextChoices):
    OPENAI = "OPAI", _("OpenAI")
    STABILITYAI = "STBAI", _("Stability AI")
    GCP = "GCP", _("Google Cloud")
    AZURE = "AZC", _("Azure Cloud")
    AWS = "AWS", _("Amazon Web Services")
