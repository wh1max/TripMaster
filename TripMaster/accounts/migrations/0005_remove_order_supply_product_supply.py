# Generated by Django 5.1.1 on 2024-09-30 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_supplier_order_supply'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='supply',
        ),
        migrations.AddField(
            model_name='product',
            name='supply',
            field=models.ManyToManyField(to='accounts.supplier'),
        ),
    ]
