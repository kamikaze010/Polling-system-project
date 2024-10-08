# Generated by Django 5.0.6 on 2024-05-10 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0014_remove_poll_expiration_date_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='desc',
            field=models.CharField(default='Hey, there this is a default text description about you that you can change on after clicking on "Edit" or going to your profile page.', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='profile_img',
            field=models.ImageField(blank=True, default='media/default.jpg', null=True, upload_to='media'),
        ),
    ]
