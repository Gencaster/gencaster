from django.contrib import admin

from .models import TextToSpeech


@admin.register(TextToSpeech)
class TextToSpeechAdmin(admin.ModelAdmin):
    list_display = (
        "uuid",
        "created_date",
        "text",
        "voice_name",
    )

    readonly_fields = [
        "uuid",
        "created_date",
        "modified_date",
        "text",
        "voice_name",
        "audio_file",
    ]

    list_filter = [
        "created_date",
        "voice_name",
    ]
