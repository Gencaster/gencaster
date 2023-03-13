from django.contrib import admin

from .models import (
    AudioFile,
    Stream,
    StreamInstruction,
    StreamPoint,
    StreamVariable,
    TextToSpeech,
)


class StreamVariableInline(admin.TabularInline):
    model = StreamVariable
    extra: int = 0


@admin.register(Stream)
class StreamAdmin(admin.ModelAdmin):
    inlines = [StreamVariableInline]

    list_display = [
        "stream_point",
        "uuid",
        "created_date",
        "active",
    ]

    list_filter = [
        "stream_point",
        "active",
    ]


@admin.register(StreamPoint)
class StreamPointAdmin(admin.ModelAdmin):
    list_display = [
        "host",
        "port",
        "last_live",
        "is_online",
    ]

    readonly_fields = [
        "host",
        "port",
        "last_live",
    ]

    list_filter = [
        "host",
    ]


@admin.register(StreamInstruction)
class StreamInstructionAdmin(admin.ModelAdmin):
    list_display = [
        "uuid",
        "stream_point",
        "modified_date",
        "state",
    ]

    list_filter = [
        "stream_point",
        "state",
        "modified_date",
    ]

    readonly_fields = [
        "state",
        "return_value",
    ]


@admin.register(AudioFile)
class AudioFileAdmin(admin.ModelAdmin):
    list_display = [
        "uuid",
        "created_date",
        "file",
    ]

    readonly_fields = [
        "uuid",
        "created_date",
        "modified_date",
    ]

    list_filter = [
        "created_date",
    ]


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
    ]

    list_filter = [
        "created_date",
        "voice_name",
    ]


@admin.register(StreamVariable)
class StreamVariableAdmin(admin.ModelAdmin):
    list_display = ("uuid", "stream", "key", "value", "stream_to_sc")

    readonly_fields = ["uuid"]

    list_filter = [
        "key",
        "stream_to_sc",
        "stream__graph",
        "stream",
        "stream__stream_point",
    ]
