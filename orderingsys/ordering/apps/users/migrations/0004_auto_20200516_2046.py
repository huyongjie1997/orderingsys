# Generated by Django 2.0.3 on 2020-05-16 12:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20200514_0951'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userinfo',
            options={'verbose_name': '用户', 'verbose_name_plural': '用户'},
        ),
    ]