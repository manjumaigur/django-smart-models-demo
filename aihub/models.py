from django.db import models
from django.utils.translation import gettext_lazy as _

from .smart_models import SmartModelMixin, OriginalTextField, SmartTextField
from .choices import APIProviders


class AIAPI(models.Model):
    name = models.CharField(
        _("name"), max_length=50, blank=False, null=False, editable=False
    )
    provider = models.CharField(
        _("api provider"),
        max_length=6,
        choices=APIProviders.choices,
        default=APIProviders.OPENAI,
    )
    configurations = models.JSONField(_("configurations"), blank=False, null=False)

    def __str__(self) -> str:
        return self.name


class Comment(SmartModelMixin):
    text = OriginalTextField(_("text"), blank=False, null=False)
    kannada_text = SmartTextField(blank=True, null=True, spell_correct=True, translate=True, target_lang="Kannada"
    )
    # summarized_text = SmartTextField(_("summarized text"), blank=True, null=True, summarize=True)
    # test_text = SmartTextField(_("test text"), blank=True, null=True, spell_correct=True, translate=True, summarize=True, emojify=True)

    def __str__(self) -> str:
        return self.text
