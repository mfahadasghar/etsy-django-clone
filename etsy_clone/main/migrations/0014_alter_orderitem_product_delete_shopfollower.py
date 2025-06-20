# Generated by Django 5.2.1 on 2025-06-10 14:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_shopfollower_delete_shoprating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='main.product'),
        ),
        migrations.DeleteModel(
            name='ShopFollower',
        ),
    ]
