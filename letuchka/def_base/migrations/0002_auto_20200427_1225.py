# Generated by Django 3.0.5 on 2020-04-27 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('def_base', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='definition',
            options={'verbose_name': 'Опредление', 'verbose_name_plural': 'Опредления'},
        ),
        migrations.AddField(
            model_name='definition',
            name='header_def',
            field=models.TextField(default='The header', max_length=140, verbose_name='Заголовок'),
        ),
    ]
