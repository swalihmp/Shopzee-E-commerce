# Generated by Django 4.1.4 on 2023-02-08 04:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_remove_userprofile_address_line_1_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_picture',
            field=models.ImageField(default='avatar.png', upload_to='UserProfile'),
        ),
    ]
