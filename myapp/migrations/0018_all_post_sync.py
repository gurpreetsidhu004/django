# Generated by Django 2.2.6 on 2019-11-01 07:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0017_data_record_excel_uploaded'),
    ]

    operations = [
        migrations.CreateModel(
            name='All_post_sync',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('record', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.Data_record')),
            ],
        ),
    ]