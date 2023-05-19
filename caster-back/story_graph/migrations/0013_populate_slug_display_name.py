# Generated by Django 4.1.3 on 2023-05-16 09:25

from django.db import migrations
from django.utils.text import slugify


def gen_slug_and_display_name(apps, schema_editor):
    Graph = apps.get_model("story_graph", "Graph")
    for row in Graph.objects.all():
        row.slug_name = slugify(row.name, allow_unicode=False)
        row.display_name = row.name
        row.save(update_fields=["slug_name", "display_name"])


class Migration(migrations.Migration):
    dependencies = [
        ("story_graph", "0012_enhance_graph_metadata"),
    ]

    operations = [
        migrations.RunPython(
            gen_slug_and_display_name, reverse_code=migrations.RunPython.noop
        )
    ]