# Generated by Django 4.1.4 on 2023-02-11 03:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminp', '0006_alter_coupon_activ_date_alter_coupon_exp_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='disc_amount',
            field=models.CharField(default=0, max_length=20),
        ),
    ]
