# Generated by Django 2.2 on 2021-03-23 13:40

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goods',
            name='detail',
            field=ckeditor.fields.RichTextField(blank=True, max_length=200, verbose_name='商品详情'),
        ),
    ]
