# Generated by Django 3.1.4 on 2020-12-21 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('natapp', '0005_auto_20201204_1913'),
    ]

    operations = [
        migrations.CreateModel(
            name='IP_list',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test', models.TextField()),
            ],
        ),
    ]
