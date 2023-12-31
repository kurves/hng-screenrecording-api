# Generated by Django 4.2.5 on 2023-09-28 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ScreenVideo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('video_file', models.FileField(upload_to='recorded_videos/')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
