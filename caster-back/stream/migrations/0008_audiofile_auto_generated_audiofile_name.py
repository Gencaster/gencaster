# Generated by Django 4.1.3 on 2023-03-16 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("stream", "0007_stream_graph_streamvariable_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="audiofile",
            name="auto_generated",
            field=models.BooleanField(
                default=True,
                help_text="Allows to separate automatic generated audio files speech to text and user uploads",
            ),
        ),
        migrations.AddField(
            model_name="audiofile",
            name="name",
            field=models.CharField(
                default="untitled",
                help_text="Acts as an identifier for humans",
                max_length=1024,
            ),
        ),
    ]
