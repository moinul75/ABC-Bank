# Generated by Django 4.2.4 on 2023-09-05 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_bank_userbankaccount_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userbankaccount',
            name='profile_picture',
            field=models.ImageField(blank=True, default='profile_image/default-profile.png', upload_to='profile_image'),
        ),
    ]