# Generated by Django 2.0 on 2018-01-16 02:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0006_auto_20180116_0018'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymenthistory',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name='image'),
        ),
    ]
