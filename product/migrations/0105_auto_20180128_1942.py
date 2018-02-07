# Generated by Django 2.0.1 on 2018-01-28 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0104_auto_20180128_1940'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cacheamazonsearch',
            name='detail_page_url',
            field=models.CharField(max_length=500, verbose_name='Detail'),
        ),
        migrations.AlterField(
            model_name='cacheamazonsearch',
            name='large_image_url',
            field=models.CharField(blank=True, max_length=400, null=True, verbose_name='Image'),
        ),
        migrations.AlterField(
            model_name='cacheamazonsearch',
            name='offer_url',
            field=models.CharField(max_length=400, verbose_name='Offer'),
        ),
        migrations.AlterField(
            model_name='cacheamazonsearch',
            name='title',
            field=models.CharField(max_length=255, verbose_name='Title'),
        ),
    ]