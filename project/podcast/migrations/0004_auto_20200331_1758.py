# Generated by Django 3.0.4 on 2020-03-31 17:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('podcast', '0003_auto_20200331_1721'),
    ]

    operations = [
        migrations.AlterField(
            model_name='podcast',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='podcasts', to=settings.AUTH_USER_MODEL),
        ),
    ]
