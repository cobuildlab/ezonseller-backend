# Generated by Django 2.0.1 on 2019-04-23 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0026_auto_20190420_1914'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymenthistory',
            name='renovate',
            field=models.BooleanField(default=False, verbose_name='Renovate'),
        ),
    ]
