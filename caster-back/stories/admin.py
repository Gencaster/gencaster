from django.contrib import admin

from .models import Story, Chapter, Block


@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ("name",)

    prepopulated_fields = {"slug": ("name",)}


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "story",
    )

    list_filter = ("story",)

    prepopulated_fields = {"slug": ("name",)}


@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "chapter",
        "text",
        "block_type",
        "active",
    )

    list_filter = (
        "chapter",
        "chapter__story",
        "block_type",
    )

    prepopulated_fields = {"slug": ("name",)}
