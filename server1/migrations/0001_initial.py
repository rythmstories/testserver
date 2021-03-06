# Generated by Django 3.1.3 on 2021-02-06 20:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tokendetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=200)),
                ('status', models.CharField(max_length=50)),
                ('lasttime', models.DateTimeField()),
                ('livestatus', models.CharField(max_length=50)),
                ('userpk', models.IntegerField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Userdetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=200)),
                ('password', models.CharField(max_length=200)),
                ('tokenid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='server1.tokendetails')),
            ],
        ),
    ]
