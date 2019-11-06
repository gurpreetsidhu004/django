# Generated by Django 2.2.5 on 2019-10-09 19:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_present_ghost_tags_hit_details'),
    ]

    operations = [
        migrations.CreateModel(
            name='Keywords_record',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keyword_name', models.CharField(max_length=250, unique=True)),
                ('keyword_image_url', models.URLField(max_length=250)),
            ],
        ),
        migrations.AddField(
            model_name='data_record',
            name='feature_image',
            field=models.URLField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='data_record',
            name='mobiledoc',
            field=models.TextField(max_length=2000, null=True),
        ),
        migrations.CreateModel(
            name='Tag_details',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_id', models.CharField(max_length=250, unique=True)),
                ('slug', models.CharField(max_length=250, unique=True)),
                ('description', models.TextField(max_length=1000, null=True)),
                ('feature_image', models.URLField(max_length=250, null=True)),
                ('visibility', models.CharField(default='public', max_length=250)),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField()),
                ('url', models.URLField(default='https://knowzone.ghostzones.ml/404/', max_length=250)),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.Keywords_record')),
            ],
        ),
        migrations.AddField(
            model_name='data_record',
            name='complete_tags',
            field=models.ManyToManyField(to='myapp.Tag_details'),
        ),
        migrations.AddField(
            model_name='data_record',
            name='keywords_with_img',
            field=models.ManyToManyField(to='myapp.Keywords_record'),
        ),
    ]
