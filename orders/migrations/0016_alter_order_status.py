# Generated by Django 4.1.7 on 2023-03-02 05:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0015_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Delivered', 'Delivered'), ('Shipped', 'Shipped'), ('New', 'New'), ('Packed', 'Packed')], default='New', max_length=20),
        ),
    ]
