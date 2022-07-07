# Generated by Django 4.0.4 on 2022-06-29 20:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0005_rename_date_good_createdat'),
    ]

    operations = [
        migrations.CreateModel(
            name='GoodImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField(default=1)),
            ],
        ),
        migrations.RemoveField(
            model_name='good',
            name='images',
        ),
        migrations.AddField(
            model_name='good',
            name='images',
            field=models.ManyToManyField(blank=True, related_name='goods', through='goods.GoodImage', to='goods.image'),
        ),
        migrations.AddField(
            model_name='goodimage',
            name='good',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.good'),
        ),
        migrations.AddField(
            model_name='goodimage',
            name='image',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.image'),
        ),
    ]