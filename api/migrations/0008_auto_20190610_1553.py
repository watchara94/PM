# Generated by Django 2.1.1 on 2019-06-10 08:53

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_userlog_points'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userlog',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2019, 6, 10, 8, 53, 57, 914274, tzinfo=utc)),
        ),
    ]
