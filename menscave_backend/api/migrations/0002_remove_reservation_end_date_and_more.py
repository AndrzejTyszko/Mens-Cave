# Generated by Django 5.1.7 on 2025-03-17 19:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reservation',
            name='end_date',
        ),
        migrations.RemoveField(
            model_name='reservation',
            name='negotiated_price',
        ),
        migrations.RemoveField(
            model_name='reservation',
            name='start_date',
        ),
        migrations.AddField(
            model_name='reservation',
            name='end_datetime',
            field=models.DateTimeField(default=datetime.datetime(2025, 3, 17, 19, 33, 47, 127039, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reservation',
            name='start_datetime',
            field=models.DateTimeField(default=datetime.datetime(2025, 3, 17, 19, 33, 55, 438605, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reservation',
            name='total_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8),
        ),
    ]
