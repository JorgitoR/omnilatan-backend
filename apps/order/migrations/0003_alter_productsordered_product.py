# Generated by Django 3.2.6 on 2021-08-30 13:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_order_payment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productsordered',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_order', to='order.orderproduct'),
        ),
    ]
