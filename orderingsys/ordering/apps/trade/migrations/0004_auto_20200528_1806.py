# Generated by Django 2.0.3 on 2020-05-28 10:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trade', '0003_auto_20200528_1757'),
    ]

    operations = [
        # migrations.RemoveField(
        #     model_name='orderinfo',
        #     name='signer_name',
        # ),
        # migrations.RemoveField(
        #     model_name='orderinfo',
        #     name='singer_mobile',
        # ),
        migrations.AlterField(
            model_name='orderinfo',
            name='address',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Address', verbose_name='收货地址'),
        ),
    ]