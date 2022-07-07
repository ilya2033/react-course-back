# Generated by Django 4.0.4 on 2022-06-24 19:24

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_remove_order_adress_order_address'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='date',
            new_name='createdAt',
        ),
        migrations.RemoveField(
            model_name='order',
            name='address',
        ),
        migrations.RemoveField(
            model_name='order',
            name='email',
        ),
        migrations.RemoveField(
            model_name='order',
            name='name',
        ),
        migrations.RemoveField(
            model_name='order',
            name='phoneNumber',
        ),
        migrations.RemoveField(
            model_name='order',
            name='surname',
        ),
        migrations.AddField(
            model_name='ordergood',
            name='createdAt',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]