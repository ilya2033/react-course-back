# Generated by Django 4.0.4 on 2022-06-29 12:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0005_rename_date_good_createdat'),
        ('authAPI', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='avatar',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='goods.image'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='name',
            field=models.CharField(default='-', max_length=50, verbose_name='name'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='nick',
            field=models.CharField(default='-', max_length=50, verbose_name='nick'),
        ),
    ]
