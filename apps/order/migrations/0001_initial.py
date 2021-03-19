# Generated by Django 2.2 on 2021-03-19 02:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OrderGoods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='删除标记')),
                ('count', models.IntegerField(default=1, verbose_name='商品数量')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='商品价格')),
                ('comment', models.TextField(verbose_name='评论')),
            ],
            options={
                'verbose_name': '订单商品',
                'verbose_name_plural': '订单商品',
                'db_table': 'shop_order_goods',
            },
        ),
        migrations.CreateModel(
            name='OrderInfo',
            fields=[
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='删除标记')),
                ('order_id', models.CharField(max_length=128, primary_key=True, serialize=False, verbose_name='订单号')),
                ('pay_method', models.SmallIntegerField(choices=[(1, '支付宝'), (2, '微信'), (3, '银行卡')], verbose_name='支付方式')),
                ('total_count', models.IntegerField(default=1, verbose_name='商品数目')),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='商品价格')),
                ('order_status', models.SmallIntegerField(choices=[(1, '待支付'), (2, '待发货'), (3, '已发货'), (4, '待评价'), (5, '已评价')], default=1, verbose_name='订单状态')),
                ('order_pay_id', models.CharField(default='', max_length=128, verbose_name='支付编号')),
            ],
            options={
                'verbose_name': '订单',
                'verbose_name_plural': '订单',
                'db_table': 'shop_order_info',
            },
        ),
        migrations.CreateModel(
            name='Transit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='删除标记')),
                ('transit', models.SmallIntegerField(choices=[('包邮', 0), ('不包邮', 10)], verbose_name='运费')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
