# Generated by Django 3.0.5 on 2020-05-08 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('def_base', '0009_auto_20200508_1246'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='definition',
            name='created_at',
        ),
        migrations.AddField(
            model_name='definition',
            name='category',
            field=models.TextField(default='The category', verbose_name='Категория'),
        ),
    ]
