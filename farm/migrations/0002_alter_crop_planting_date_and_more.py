# Generated by Django 5.0.2 on 2024-03-30 09:12

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('farm', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='crop',
            name='planting_date',
            field=models.DateField(default=datetime.date(2024, 3, 30)),
        ),
        migrations.AlterField(
            model_name='employee',
            name='date_employed',
            field=models.DateField(blank=True, default=datetime.date(2024, 3, 30), validators=[django.core.validators.RegexValidator(code='invalid_date_format', message='Date must be in the format YYYY-MM-DD', regex='^\\d{4}-\\d{2}-\\d{2}$')]),
        ),
        migrations.AlterField(
            model_name='expense',
            name='date',
            field=models.DateField(default=datetime.date(2024, 3, 30)),
        ),
        migrations.AlterField(
            model_name='goal',
            name='date',
            field=models.DateField(default=datetime.date(2024, 3, 30)),
        ),
        migrations.AlterField(
            model_name='sale',
            name='date',
            field=models.DateField(default=datetime.date(2024, 3, 30)),
        ),
        migrations.AlterField(
            model_name='task',
            name='date',
            field=models.DateField(default=datetime.date(2024, 3, 30)),
        ),
    ]
