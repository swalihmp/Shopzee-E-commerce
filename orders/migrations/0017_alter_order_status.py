# Generated by Django 4.1.7 on 2023-03-02 05:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0016_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Delivered', 'Delivered'), ('New', 'New'), ('Shipped', 'Shipped'), ('Packed', 'Packed')], default='New', max_length=20),
        ),
    ]
