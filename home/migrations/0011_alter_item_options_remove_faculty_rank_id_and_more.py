# Generated by Django 4.2.14 on 2024-08-05 21:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_alter_faculty_item_status'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='item',
            options={},
        ),
        migrations.RemoveField(
            model_name='faculty',
            name='rank_id',
        ),
        migrations.RemoveField(
            model_name='item',
            name='item_description',
        ),
        migrations.RemoveField(
            model_name='item',
            name='item_no',
        ),
        migrations.RemoveField(
            model_name='item',
            name='position_id',
        ),
        migrations.AddField(
            model_name='faculty',
            name='employment_status',
            field=models.CharField(blank=True, choices=[('Retired', 'Retired'), ('Resigned', 'Resigned'), ('AWOL', 'AWOL'), ('Study', 'Study'), ('Indefinite', 'Indefinite'), ('Terminated', 'Terminated'), ('Others', 'Others')], max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='faculty',
            name='employment_type',
            field=models.CharField(choices=[('Teaching', 'Teaching'), ('None-Teaching', 'None-Teaching')], default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='faculty',
            name='item_no',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='faculty',
            name='position_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='position_item', to='home.position'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='faculty',
            name='item_status',
            field=models.CharField(choices=[('COS', 'COS'), ('JO', 'JO'), ('Permanent', 'Permanent'), ('Vacant', 'Vacant')], max_length=50),
        ),
        migrations.AlterField(
            model_name='position',
            name='position_name',
            field=models.CharField(max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='position',
            name='position_short_name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]