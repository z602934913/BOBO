# Generated by Django 4.0.3 on 2022-04-14 06:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('commodity', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='commoditytype',
            options={'verbose_name': '种类', 'verbose_name_plural': '种类'},
        ),
        migrations.AlterModelTable(
            name='commoditytype',
            table='df_goods_type',
        ),
    ]
