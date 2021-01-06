# Generated by Django 3.1.4 on 2021-01-01 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anpr', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='camera',
            name='url',
            field=models.CharField(help_text='Functioning RTSP link(rtsp://localhost:8554/ds-test) or Path to Local Video(/home/user/vid.mp4.', max_length=400),
        ),
        migrations.AlterField(
            model_name='camera',
            name='video_display',
            field=models.BooleanField(default=False, help_text='Tick to turn it on. Enables video display with bounding boxes and FPS for debugging purposes. Remember to disable before Deployment.'),
        ),
    ]
