# Generated by Django 4.0.2 on 2022-09-30 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("stream", "0002_janus_info"),
    ]

    operations = [
        migrations.AlterField(
            model_name="streampoint",
            name="janus_in_port",
            field=models.IntegerField(
                blank=True,
                help_text="RTP port where Janus streams the audio its received from user",
                null=True,
                verbose_name="Jauns in port",
            ),
        ),
        migrations.AlterField(
            model_name="streampoint",
            name="janus_in_room",
            field=models.IntegerField(
                blank=True,
                help_text="Audiobridge room ID under which Janus can send audio to SuperCollider",
                null=True,
                verbose_name="Janus in room",
            ),
        ),
        migrations.AlterField(
            model_name="streampoint",
            name="janus_out_port",
            field=models.IntegerField(
                blank=True,
                help_text="RTP port where SuperCollider/gstreamer streams its audio to Janus",
                null=True,
                verbose_name="Janus out port",
            ),
        ),
        migrations.AlterField(
            model_name="streampoint",
            name="janus_out_room",
            field=models.IntegerField(
                blank=True,
                help_text="Streaming room ID under which Janus serves audio from SuperCollider",
                null=True,
                verbose_name="Jauns out room",
            ),
        ),
        migrations.AlterField(
            model_name="streampoint",
            name="janus_public_ip",
            field=models.CharField(
                blank=True,
                help_text="IP or Hostname under which the janus instance is reachable",
                max_length=128,
                null=True,
                verbose_name="Janus public IP",
            ),
        ),
        migrations.AlterField(
            model_name="streampoint",
            name="last_live",
            field=models.DateTimeField(
                help_text="Last live signal from SuperCollider server",
                null=True,
                verbose_name="Last live signal",
            ),
        ),
        migrations.AlterField(
            model_name="streampoint",
            name="sc_name",
            field=models.CharField(
                help_text="Internal name of the SuperCollider instance on the host, necessary for gstreamer",
                max_length=128,
                null=True,
                verbose_name="SuperCollider name",
            ),
        ),
        migrations.AlterField(
            model_name="streampoint",
            name="use_input",
            field=models.BooleanField(
                default=False,
                help_text="Accepts to send audio input",
                verbose_name="Use input",
            ),
        ),
    ]