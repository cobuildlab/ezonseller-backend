# Generated by Django 2.0.1 on 2018-01-28 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0103_cacheamazonsearch'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cacheamazonsearch',
            name='availability',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Availability'),
        ),
        migrations.AlterField(
            model_name='cacheamazonsearch',
            name='large_image_url',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Image'),
        ),
        migrations.AlterField(
            model_name='cacheamazonsearch',
            name='price_and_currency',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Price'),
        ),
    ]
