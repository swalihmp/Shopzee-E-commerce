# Generated by Django 4.1.7 on 2023-03-02 05:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0017_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Shipped', 'Shipped'), ('Packed', 'Packed'), ('Delivered', 'Delivered'), ('New', 'New')], default='New', max_length=20),
        ),
    ]
