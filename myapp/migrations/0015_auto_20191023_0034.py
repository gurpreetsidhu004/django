# Generated by Django 2.2.6 on 2019-10-23 00:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0014_auto_20191023_0033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='data_record',
            name='title',
            field=models.CharField(max_length=250),
        ),
    ]
