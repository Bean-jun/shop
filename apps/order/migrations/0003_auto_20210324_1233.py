# Generated by Django 2.2 on 2021-03-24 04:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_auto_20210319_1029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transit',
            name='transit',
            field=models.SmallIntegerField(choices=[(0, '包邮'), (10, '不包邮')], verbose_name='运费'),
        ),
    ]
