# Generated by Django 4.1.3 on 2023-03-14 19:18

import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("stream", "0007_stream_graph_streamvariable_and_more"),
        ("story_graph", "0008_delete_graphsession"),
    ]

    operations = [
        migrations.AlterField(
            model_name="scriptcell",
            name="cell_type",
            field=models.CharField(
                choices=[
                    ("markdown", "Markdown"),
                    ("python", "Python"),
                    ("supercollider", "SuperCollider"),
                    ("comment", "Comment"),
                    ("audio", "Audio"),
                ],
                default="comment",
                max_length=128,
                verbose_name="Cell type",
            ),
        ),
        migrations.CreateModel(
            name="AudioCell",
            fields=[
                (
                    "uuid",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                (
                    "playback",
                    models.CharField(
                        choices=[
                            ("sync_playback", "Sync playback"),
                            ("async_playback", "Async playback"),
                        ],
                        default="sync_playback",
                        max_length=512,
                    ),
                ),
                ("volume", models.FloatField(default=0.2)),
                (
                    "audio_file",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="audio_cells",
                        to="stream.audiofile",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="scriptcell",
            name="audio_cell",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="script_cell",
                to="story_graph.audiocell",
            ),
        ),
    ]