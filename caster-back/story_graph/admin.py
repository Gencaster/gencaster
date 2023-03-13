from django.contrib import admin

from .models import Edge, Graph, Node, ScriptCell


class NodeInline(admin.TabularInline):
    model = Node
    extra: int = 0


class InEdgeInline(admin.TabularInline):
    model = Edge
    extra = 1
    fk_name: str = "in_node"


class OutEdgeInline(admin.TabularInline):
    model = Edge
    extra = 1
    fk_name: str = "out_node"


class ScriptCellInline(admin.TabularInline):
    model = ScriptCell
    extra: int = 1


@admin.register(Graph)
class GraphAdmin(admin.ModelAdmin):
    inlines = [NodeInline]
    list_display = [
        "name",
        "uuid",
    ]


@admin.register(Node)
class NodeAdmin(admin.ModelAdmin):
    inlines = [ScriptCellInline, InEdgeInline, OutEdgeInline]
    list_display = [
        "name",
        "graph",
        "is_entry_node",
    ]

    list_filter = [
        "graph",
        "is_entry_node",
    ]


@admin.register(Edge)
class EdgeAdmin(admin.ModelAdmin):
    list_display = [
        "uuid",
        "in_node",
        "out_node",
    ]

    list_filter = [
        "in_node__graph",
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

    readonly_fields = [
        "uuid",
    ]
