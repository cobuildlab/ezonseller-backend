# Generated by Django 2.0 on 2018-01-16 03:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0008_paymenthistory_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymenthistory',
            name='id_card',
            field=models.IntegerField(blank=True, null=True, verbose_name='id_card'),
        ),
        migrations.AddField(
            model_name='paymenthistory',
            name='id_plan',
            field=models.IntegerField(blank=True, null=True, verbose_name='id_plan'),
        ),
    ]
