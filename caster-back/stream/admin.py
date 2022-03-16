from django.contrib import admin

from .models import Stream, StreamInstruction, StreamPoint


@admin.register(Stream)
class StreamAdmin(admin.ModelAdmin):
    pass


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
