# Generated by Django 2.0.3 on 2020-05-14 01:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20200428_1402'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='balance',
            field=models.IntegerField(default=0, verbose_name='用户余额'),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='revenue',
            field=models.IntegerField(default=0, verbose_name='用户金额'),
        ),
    ]