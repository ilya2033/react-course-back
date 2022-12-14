# Generated by Django 4.0.4 on 2022-07-20 13:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0006_goodimage_alter_good_images_goodimage_good_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='goodimage',
            options={'ordering': ('order',)},
        ),
        migrations.AlterField(
            model_name='good',
            name='description',
            field=models.CharField(blank=True, default='', max_length=5000, verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='goodimage',
            name='good',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='GoodImages', to='goods.good'),
        ),
    ]
