# Generated by Django 4.1.7 on 2023-02-28 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0025_remove_product_images_delete_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='images',
            field=models.ImageField(default=0, upload_to='photos/products'),
            preserve_default=False,
        ),
    ]
