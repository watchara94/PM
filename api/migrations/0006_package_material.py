# Generated by Django 2.1.1 on 2019-05-31 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20190531_1242'),
    ]

    operations = [
        migrations.AddField(
            model_name='package',
            name='material',
            field=models.TextField(default='Plastic'),
        ),
    ]
