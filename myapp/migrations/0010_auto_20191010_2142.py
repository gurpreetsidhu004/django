# Generated by Django 2.2.5 on 2019-10-10 21:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_auto_20191009_2030'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='data_record',
            name='keywords_with_img',
        ),
        migrations.AlterField(
            model_name='tag_details',
            name='feature_image',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.DeleteModel(
            name='Keywords_record',
        ),
    ]
