# Generated by Django 2.0.3 on 2020-04-28 06:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='avatar',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='头像'),
        ),
    ]