# Generated by Django 2.2.6 on 2019-10-31 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0016_auto_20191023_0036'),
    ]

    operations = [
        migrations.AddField(
            model_name='data_record',
            name='excel_uploaded',
            field=models.BooleanField(default=False),
        ),
    ]
