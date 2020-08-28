# Generated by Django 2.0.3 on 2020-04-27 08:58

import DjangoUeditor.models
import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='菜名')),
                ('comment_count', models.IntegerField(default=0, verbose_name='评论数')),
                ('month_count', models.IntegerField(default=0, verbose_name='月销售量')),
                ('status', models.IntegerField(default=0, verbose_name='状态')),
                ('price', models.FloatField(default=0, verbose_name='价格')),
                ('summary', DjangoUeditor.models.UEditorField(default=',settings={}, command=None,', verbose_name='介绍')),
                ('food_image', models.ImageField(blank=True, null=True, upload_to='food/images/', verbose_name='封面图')),
                ('created_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '菜名',
                'verbose_name_plural': '菜名',
            },
        ),
        migrations.CreateModel(
            name='FoodCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', help_text='类别名', max_length=30, verbose_name='类别名')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '菜品类别',
                'verbose_name_plural': '菜品类别',
            },
        ),
        migrations.CreateModel(
            name='FoodDetailsImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('food_detail_image', models.ImageField(blank=True, null=True, upload_to='food/images/', verbose_name='菜品详细图')),
                ('created_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('food', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='food', to='food.Food', verbose_name='菜品名')),
            ],
            options={
                'verbose_name': '菜品详细图',
                'verbose_name_plural': '菜品详细图',
            },
        ),
        migrations.AddField(
            model_name='food',
            name='foodcategory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='foodcategory', to='food.FoodCategory', verbose_name='菜品类别'),
        ),
    ]
