# Generated by Django 5.0 on 2024-02-09 00:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_cartproduct_quantity'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductSupply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=100)),
                ('added_quantity', models.IntegerField()),
                ('added_time', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.product')),
            ],
        ),
        migrations.DeleteModel(
            name='ProductInStock',
        ),
        migrations.DeleteModel(
            name='StockRegion',
        ),
    ]