# Generated by Django 4.2.14 on 2024-08-04 12:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_remove_academicrank_date_end_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='faculty',
            name='department_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='department_faculty', to='home.department'),
        ),
        migrations.AlterField(
            model_name='faculty',
            name='education',
            field=models.CharField(blank=True, choices=[('Elementary', 'Elementary'), ('Secondary', 'Secondary'), ('College', 'College'), ('Graduated', 'College graduate'), ('Master', 'Master'), ('Doctor', 'Doctor')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='faculty',
            name='faculty_no',
            field=models.CharField(blank=True, max_length=50, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='faculty',
            name='first_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='faculty',
            name='gender',
            field=models.CharField(blank=True, choices=[('Male', 'Male'), ('Female', 'Female')], max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='faculty',
            name='item_status',
            field=models.CharField(blank=True, choices=[('COS', 'COS'), ('Permanent', 'Permanent'), ('Vacant', 'Vacant')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='faculty',
            name='last_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='faculty',
            name='rank_id',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rank_academicRank', to='home.item'),
        ),
    ]