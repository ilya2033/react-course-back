# Generated by Django 4.0.4 on 2022-06-24 21:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0004_alter_good_amount_alter_good_description_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='good',
            old_name='date',
            new_name='createdAt',
        ),
    ]
