# Generated by Django 4.0.3 on 2022-04-17 03:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ordercommodity',
            options={'verbose_name': '订单商品表', 'verbose_name_plural': '订单商品表'},
        ),
        migrations.AlterModelOptions(
            name='orderinfo',
            options={'verbose_name': '订单表', 'verbose_name_plural': '订单表'},
        ),
    ]
