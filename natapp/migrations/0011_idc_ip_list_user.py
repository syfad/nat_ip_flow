# Generated by Django 3.1.4 on 2020-12-21 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('natapp', '0010_auto_20201221_1537'),
    ]

    operations = [
        migrations.CreateModel(
            name='IDC_IP_LIST',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('IDC', models.CharField(max_length=64)),
                ('POOL1', models.TextField(db_index=True)),
                ('POOL2', models.TextField(db_index=True)),
                ('POOL3', models.TextField(db_index=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('nid', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(db_index=True, max_length=32)),
                ('passwd', models.GenericIPAddressField(db_index=True)),
            ],
        ),
    ]
