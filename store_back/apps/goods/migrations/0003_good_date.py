# Generated by Django 4.0.4 on 2022-05-30 20:08

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0002_alter_good_amount_remove_good_images_good_images'),
    ]

    operations = [
        migrations.AddField(
            model_name='good',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
