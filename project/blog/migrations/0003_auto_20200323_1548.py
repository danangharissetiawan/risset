# Generated by Django 2.2.10 on 2020-03-23 15:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20200323_1540'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='kategori',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.Kategori'),
        ),
    ]
