# Generated by Django 2.2.5 on 2019-10-01 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='data_record',
            name='file_path',
            field=models.URLField(max_length=250),
        ),
    ]