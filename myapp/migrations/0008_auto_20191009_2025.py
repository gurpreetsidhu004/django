# Generated by Django 2.2.5 on 2019-10-09 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_data_record_iframe'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag_details',
            name='meta_description',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='tag_details',
            name='meta_title',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]