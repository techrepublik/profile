# Generated by Django 4.2.14 on 2024-08-03 22:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='department',
            old_name='department_short',
            new_name='department_short_name',
        ),
        migrations.RenameField(
            model_name='position',
            old_name='position_short',
            new_name='position_short_name',
        ),
        migrations.RenameField(
            model_name='unit',
            old_name='unit_short',
            new_name='unit_short_name',
        ),
    ]
