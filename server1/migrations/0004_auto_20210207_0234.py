# Generated by Django 3.1.3 on 2021-02-06 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server1', '0003_auto_20210207_0232'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tokendetails',
            name='userpk',
            field=models.IntegerField(blank=True, default=0),
            preserve_default=False,
        ),
    ]