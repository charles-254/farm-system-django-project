# Generated by Django 5.0.2 on 2024-03-27 05:10

import datetime
import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('farm', '0008_task'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='crop',
            name='planting_date',
            field=models.DateField(default=datetime.date(2024, 3, 27)),
        ),
        migrations.AlterField(
            model_name='employee',
            name='date_employed',
            field=models.DateField(blank=True, default=datetime.date(2024, 3, 27), validators=[django.core.validators.RegexValidator(code='invalid_date_format', message='Date must be in the format YYYY-MM-DD', regex='^\\d{4}-\\d{2}-\\d{2}$')]),
        ),
        migrations.AlterField(
            model_name='goal',
            name='date',
            field=models.DateField(default=datetime.date(2024, 3, 27)),
        ),
        migrations.AlterField(
            model_name='task',
            name='date',
            field=models.DateField(default=datetime.date(2024, 3, 27)),
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('sale_id', models.AutoField(primary_key=True, serialize=False)),
                ('category', models.CharField(max_length=255)),
                ('product_name', models.CharField(max_length=255)),
                ('quantity', models.PositiveIntegerField()),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('date', models.DateField(default=datetime.date(2024, 3, 27))),
                ('notes', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
