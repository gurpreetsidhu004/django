# Generated by Django 2.1.1 on 2019-10-18 01:08

from django.db import migrations, models
import django.db.models.deletion
import django_mysql.models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0012_auto_20191014_2049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='data_record',
            name='categories',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.Category'),
        ),
        migrations.AlterField(
            model_name='data_record',
            name='file_path',
            field=models.URLField(max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='data_record',
            name='keywords',
            field=models.TextField(max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='data_record',
            name='keywords_with_links',
            field=django_mysql.models.JSONField(default=dict, null=True),
        ),
    ]
