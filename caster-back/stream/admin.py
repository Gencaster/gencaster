from django.contrib import admin

from .models import Stream, StreamInstruction, StreamPoint


@admin.register(Stream)
class StreamAdmin(admin.ModelAdmin):
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
    pass
