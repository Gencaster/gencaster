# Generated by Django 4.1.3 on 2023-05-16 09:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("story_graph", "0011_alter_graph_options_node_is_blocking_node"),
    ]

    operations = [
        migrations.AddField(
            model_name="graph",
            name="about_text",
            field=models.TextField(
                default="",
                help_text="Text about the graph which can be accessed during a stream - only if this is set",
                verbose_name="About text (markdown)",
            ),
        ),
        migrations.AddField(
            model_name="graph",
            name="display_name",
            field=models.CharField(
                default="",
                help_text="Will be used as a display name in the frontend",
                max_length=512,
                verbose_name="Display name",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="graph",
            name="end_text",
            field=models.TextField(
                default="",
                help_text="Text which will be displayed at the end of a stream",
                verbose_name="End text (markdown)",
            ),
        ),
        migrations.AddField(
            model_name="graph",
            name="public_visible",
            field=models.BooleanField(
                default=True,
                help_text="If the graph is not public it will not be listed in the frontend, yet it is still accessible via URL",
                verbose_name="Public visible?",
            ),
        ),
        migrations.AddField(
            model_name="graph",
            name="slug_name",
            field=models.SlugField(
                default=2,
                help_text="Will be used as a URL",
                max_length=256,
                null=True,
                verbose_name="Slug name",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="graph",
            name="start_text",
            field=models.TextField(
                default="",
                help_text="Text about the graph which will be displayed at the start of a stream - only if this is set",
                verbose_name="Start text (markdown)",
            ),
        ),
        migrations.AddField(
            model_name="graph",
            name="template_name",
            field=models.CharField(
                choices=[
                    ("default", "Default template"),
                    ("drifter", "Drifter template"),
                ],
                default="default",
                help_text="Allows to switch to a different template in the frontend with different connection flows or UI",
                max_length=255,
                verbose_name="Frontend template",
            ),
        ),
    ]