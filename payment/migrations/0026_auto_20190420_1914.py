# Generated by Django 2.0.1 on 2019-04-20 23:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0025_paymenthistory_days_free'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymenthistory',
            name='days_free',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='days_free'),
        ),
    ]
