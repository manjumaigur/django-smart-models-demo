from typing import Any
from django.db import models
from django.utils.translation import gettext_lazy as _
from loguru import logger

from .apis import translate_text, summarize_text, spell_correct_text, emojify_text
from .choices import APIProviders


def _validate_text_field_arguments(**kwargs) -> None:
    if kwargs["translate"] and kwargs["target_lang"] is None:
        raise Exception("value for 'target_lang' has to specified when translate=True")


class SmartModelMixin(models.Model):
    class Meta:
        abstract = True

    def get_original_text_field(self):
        for field in self._meta.fields:
            if isinstance(field, OriginalTextField):
                return field

        return None

    def get_smart_text_field(self):
        for field in self._meta.fields:
            if isinstance(field, SmartTextField):
                return field

        return None

    def save(self, *args, **kwargs) -> None:
        original_text_field = self.get_original_text_field()
        smart_text_field = self.get_smart_text_field()
        processed_text = None
        if original_text_field is not None:
            processed_text = getattr(self, original_text_field.attname)
        elif smart_text_field is not None:
            processed_text = getattr(self, smart_text_field.attname)
        else:
            pass

        api_provider = smart_text_field.api_provider
        if smart_text_field.spell_correct:
            processed_text = spell_correct_text(
                processed_text, api_provider=api_provider
            )
        if smart_text_field.summarize:
            processed_text = summarize_text(
                processed_text, api_provider=api_provider
            )
        if smart_text_field.translate:
            processed_text = translate_text(
                processed_text,
                target_language=smart_text_field.target_lang,
                api_provider=api_provider,
            )
        if smart_text_field.emojify:
            processed_text = emojify_text(
                processed_text, api_provider=api_provider
            )
        self.__dict__[smart_text_field.attname] = processed_text
        return super().save(*args, **kwargs)


class OriginalTextField(models.TextField):
    pass


class SmartTextField(models.TextField):

    description = "smart models.TextField"

    def __init__(
        self,
        spell_correct: bool = False,
        translate: bool = False,
        target_lang: str = None,
        summarize: bool = False,
        emojify: bool = False,
        api_provider: APIProviders = APIProviders.OPENAI,
        *args,
        **kwargs,
    ):
        """
        to: str, is only used when translate = True
        Order of execution: correct_spelling -> summarize -> translate -> emojify
        """
        # TODO: Support for multiple tasks in one field
        _validate_text_field_arguments(
            spell_correct=spell_correct,
            translate=translate,
            summarize=summarize,
            target_lang=target_lang,
            emojify=emojify,
        )
        self.spell_correct = spell_correct
        self.translate = translate
        self.target_lang = target_lang
        self.summarize = summarize
        self.emojify = emojify
        self.api_provider = api_provider
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        # Only include kwarg if it's not the default
        if not self.spell_correct:
            kwargs["spell_correct"] = self.spell_correct
        if not self.translate and self.target_lang is not None:
            kwargs["translate"] = self.translate
            kwargs["target_lang"] = self.target_lang
        if not self.summarize:
            kwargs["summarize"] = self.summarize
        if not self.emojify:
            kwargs["emojify"] = self.emojify
        kwargs["api_provider"] = self.api_provider
        return name, path, args, kwargs


# class TranslateMixin(BaseLanguageModelMixin):
#     class Meta:
#         abstract = True

#     @classmethod
#     def get_translated_text_field(cls):
#         for field in cls._meta.fields:
#             if isinstance(field, TranslatedTextField):
#                 return field.attname

#     def translate(self, to: str, provider: APIProviders = APIProviders.OPENAI):
#         original_text = getattr(self, self.get_original_text_field())
#         translated_text_field_name = self.get_translated_text_field()
#         self.__dict__[translated_text_field_name] = translate_text(
#             original_text, to=to, api_provider=provider
#         )
#         self.save(update_fields=[translated_text_field_name])


# class SummaryMixin(BaseLanguageModelMixin):
#     class Meta:
#         abstract = True

#     @classmethod
#     def get_summarized_text_field(cls):
#         for field in cls._meta.fields:
#             if isinstance(field, TranslatedTextField):
#                 return field.attname

#     def summarize(self, provider: APIProviders = APIProviders.OPENAI):
#         original_text = getattr(self, self.get_original_text_field())
#         summarized_text_field_name = self.get_summarized_text_field()
#         self.__dict__[summarized_text_field_name] = summarize_text(
#             original_text, api_provider=provider
#         )
#         self.save(update_fields=[summarized_text_field_name])
