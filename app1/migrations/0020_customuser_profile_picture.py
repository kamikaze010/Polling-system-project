# Generated by Django 5.0.6 on 2024-05-17 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0019_profile_address_profile_gender_profile_mobile_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pictures/'),
        ),
    ]
