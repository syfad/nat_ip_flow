# Generated by Django 3.1.4 on 2020-12-22 04:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('natapp', '0012_idc_ip_list_pool4'),
    ]

    operations = [
        migrations.AlterField(
            model_name='idc_ip_list',
            name='POOL4',
            field=models.TextField(db_index=True),
        ),
    ]
