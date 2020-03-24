# Generated by Django 2.2.10 on 2020-03-24 06:18

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0004_auto_20200323_1638'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='archive',
            field=models.ManyToManyField(blank=True, null=True, related_name='archives', to=settings.AUTH_USER_MODEL),
        ),
    ]