# Generated by Django 2.0.3 on 2020-05-28 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0002_auto_20200516_2046'),
    ]

    operations = [
        migrations.AddField(
            model_name='food',
            name='courier_type',
            field=models.CharField(choices=[('顺丰快递', '15.00.00'), ('圆通快递', '10.00'), ('韵达快递', '8.00'), ('京东快递', '15.00'), ('邮政快递', '6.00'), ('包邮', '0.00')], default='包邮', max_length=10, verbose_name='快递类型'),
        ),
        migrations.AddField(
            model_name='food',
            name='yun_price',
            field=models.FloatField(default=0.0, verbose_name='价格'),
        ),
        migrations.AlterField(
            model_name='food',
            name='status',
            field=models.IntegerField(default=0, verbose_name='库存数'),
        ),
    ]
