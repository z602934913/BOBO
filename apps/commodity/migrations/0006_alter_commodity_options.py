# Generated by Django 4.0.3 on 2022-04-14 07:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('commodity', '0005_alter_commdityimage_options_alter_commodity_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='commodity',
            options={'verbose_name': '商品SPU', 'verbose_name_plural': '商品SPU'},
        ),
    ]
