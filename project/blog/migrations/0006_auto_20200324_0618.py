# Generated by Django 2.2.10 on 2020-03-24 06:18

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_post_archive'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='archive',
            field=models.ManyToManyField(blank=True, related_name='archives', to=settings.AUTH_USER_MODEL),
        ),
    ]
