# Generated by Django 3.0.5 on 2020-10-24 04:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('barberapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='barberaddress',
            name='name',
            field=models.CharField(default='irfan', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='useraddress',
            name='name',
            field=models.CharField(default='irfan', max_length=50),
            preserve_default=False,
        ),
    ]
