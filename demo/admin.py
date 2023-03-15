from django.contrib import admin

from .models import (Blog, Comment, EmojiComment, MultiSpeechToText,
                     SpeechToText, SpeechTranslation)


class BlogAdmin(admin.ModelAdmin):
    readonly_fields = ("display_thumbnail",)


admin.site.register(Comment)
admin.site.register(EmojiComment)
admin.site.register(Blog, BlogAdmin)
admin.site.register(SpeechToText)
admin.site.register(SpeechTranslation)
admin.site.register(MultiSpeechToText)
