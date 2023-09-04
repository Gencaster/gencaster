from django.contrib import admin

from .models import AudioCell, Edge, Graph, Node, NodeDoor, ScriptCell


class NodeInline(admin.TabularInline):
    model = Node
    extra: int = 0


class NodeDoorInline(admin.TabularInline):
    model = NodeDoor
    extra = 1
    fk_name = "node"


class ScriptCellInline(admin.TabularInline):
    model = ScriptCell
    extra: int = 1


@admin.register(NodeDoor)
class NodeDoorAdmin(admin.ModelAdmin):
    list_display = [
        "uuid",
        "node",
        "name",
        "door_type",
        "is_default",
    ]

    autocomplete_fields = [
        "node",
    ]

    search_fields = [
        "name",
        "node__graph__name",
        "node__name",
    ]

    list_filter = [
        "door_type",
        "node__graph",
        "is_default",
    ]


@admin.register(Graph)
class GraphAdmin(admin.ModelAdmin):
    inlines = [NodeInline]
    list_display = [
        "name",
        "display_name",
        "slug_name",
        "uuid",
        "public_visible",
    ]

    search_fields = [
        "name",
        "display_name",
        "slug_name",
    ]

    prepopulated_fields = {
        "slug_name": ["name"],
        "display_name": ["name"],
    }

    list_filter = ["public_visible"]


@admin.register(Node)
class NodeAdmin(admin.ModelAdmin):
    inlines = [ScriptCellInline, NodeDoorInline]
    list_display = [
        "name",
        "graph",
        "is_entry_node",
        "is_blocking_node",
    ]

    list_filter = [
        "graph",
        "is_entry_node",
        "is_blocking_node",
    ]

    search_fields = [
        "name",
        "graph__name",
    ]

    autocomplete_fields = [
        "graph",
    ]


@admin.register(Edge)
class EdgeAdmin(admin.ModelAdmin):
    list_display = [
        "uuid",
        "in_node_door",
        "out_node_door",
    ]

    search_fields = [
        "in_node_door__node__name",
        "out_node_door__node__name",
    ]

    autocomplete_fields = [
        "in_node_door",
        "out_node_door",
    ]

    list_filter = [
        "in_node_door__node__graph",
    ]


@admin.register(ScriptCell)
class ScriptCellAdmin(admin.ModelAdmin):
    list_display = [
        "node",
        "cell_order",
        "cell_type",
    ]

    list_filter = [
        "node__graph",
        "cell_type",
    ]

    search_fields = [
        "node__name",
    ]

    readonly_fields = [
        "uuid",
    ]

    autocomplete_fields = [
        "node",
    ]


@admin.register(AudioCell)
class AudioCellAdmin(admin.ModelAdmin):
    list_display = ["uuid", "audio_file", "playback"]

    readonly_fields = ["uuid"]

    search_fields = [
        "uuid",
        "node__name",
    ]

    list_filter = [
        "playback",
        "script_cell__node__graph",
        "script_cell__node",
    ]

    autocomplete_fields = [
        "audio_file",
    ]
