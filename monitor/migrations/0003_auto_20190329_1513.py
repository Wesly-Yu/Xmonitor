# Generated by Django 2.1.5 on 2019-03-29 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0002_auto_20190329_1508'),
    ]

    operations = [
        migrations.AlterField(
            model_name='serviceindex',
            name='data_type',
            field=models.CharField(choices=[('int', 'int'), ('str', 'str'), ('float', 'float')], default='int', max_length=64, verbose_name='数据指标类型'),
        ),
    ]