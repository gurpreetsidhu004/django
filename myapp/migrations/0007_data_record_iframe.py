# Generated by Django 2.2.5 on 2019-10-09 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_auto_20191009_1957'),
    ]

    operations = [
        migrations.AddField(
            model_name='data_record',
            name='iframe',
            field=models.BooleanField(default=False),
        ),
    ]
