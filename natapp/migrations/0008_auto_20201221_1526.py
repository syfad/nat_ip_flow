# Generated by Django 3.1.4 on 2020-12-21 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('natapp', '0007_auto_20201221_1524'),
    ]

    operations = [
        migrations.AlterField(
            model_name='idc_ip_list',
            name='POOL1',
            field=models.TextField(db_index=True, max_length=1000),
        ),
    ]
