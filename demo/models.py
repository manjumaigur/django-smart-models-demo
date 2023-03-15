from django.db import models
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from smart_models.fields import (AudioToTextField, SmartImageField,
                                 SmartTextField)
from smart_models.models import AudioAIModel, ImageAIModel, TextAIModel


def get_audio_file_path(instance, filename) -> str:
    return f"audio/{filename}"


def get_image_file_path(instance, filename) -> str:
    return f"image/{filename}"


class Comment(TextAIModel):
    text = models.TextField(_("text"), blank=False, null=False)
    kannada_text = SmartTextField(
        blank=True,
        null=True,
        data_fields=["text"],
        spell_correct=True,
        translate=True,
        target_lang="Kannada",
    )
    # summarized_text = SmartTextField(_("summarized text"), blank=True, null=True, summarize=True)
    # test_text = SmartTextField(_("test text"), blank=True, null=True, spell_correct=True, translate=True, summarize=True, emojify=True)

    def __str__(self) -> str:
        return self.text


class EmojiComment(TextAIModel):
    text = models.TextField(_("text"), blank=False, null=False)
    emojified_text = SmartTextField(
        blank=True, null=True, data_fields=["text"], spell_correct=True, emojify=True
    )

    def __str__(self) -> str:
        return self.text


class Blog(TextAIModel, ImageAIModel):
    article = models.TextField(_("text"), blank=False, null=False)
    title = SmartTextField(
        blank=True,
        null=True,
        data_fields=["article"],
        spell_correct=True,
        generate_title=True,
        max_title_length=50,
    )
    thumbnail = SmartImageField(
        blank=True,
        null=True,
        upload_to=get_image_file_path,
        data_fields=["article"],
        thumbnail=True,
        image_height=512,
        image_width=512,
        image_extension="png",
    )

    def __str__(self) -> str:
        return self.title

    def display_thumbnail(self):
        html = '<img src="{img}">'
        if self.thumbnail:
            return format_html(html, img=self.thumbnail.url)
        return format_html("<p>Thumbnail not yet generated.<p>")

    display_thumbnail.short_description = "Thumbnail preview"


class SpeechToText(AudioAIModel):
    audio_file = models.FileField(
        blank=False, null=False, upload_to=get_audio_file_path
    )
    transcribed_audio = AudioToTextField(
        blank=True, null=True, data_fields=["audio_file"], transcribe=True
    )

    def __str__(self) -> str:
        return str(self.id)


class MultiSpeechToText(AudioAIModel):
    audio_file1 = models.FileField(
        blank=False, null=False, upload_to=get_audio_file_path
    )
    audio_file2 = models.FileField(
        blank=False, null=False, upload_to=get_audio_file_path
    )
    transcribed_audio = AudioToTextField(
        blank=True,
        null=True,
        data_fields=["audio_file1", "audio_file2"],
        transcribe=True,
    )

    def __str__(self) -> str:
        return str(self.id)


class SpeechTranslation(AudioAIModel):
    audio_file = models.FileField(
        blank=False, null=False, upload_to=get_audio_file_path
    )
    translated_audio = AudioToTextField(
        blank=True, null=True, data_fields=["audio_file"], translate=True
    )

    def __str__(self) -> str:
        return str(self.id)
