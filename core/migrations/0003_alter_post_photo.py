# Generated by Django 4.1.4 on 2022-12-28 06:27

import core.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_post_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='photo',
            field=models.ImageField(blank=True, editable=False, null=True, upload_to=core.models.post_image_file_path),
        ),
    ]
