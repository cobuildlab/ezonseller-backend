# Generated by Django 2.0 on 2018-01-15 18:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0004_plansubscription_duration'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='creditcard',
            name='date_creation',
        ),
        migrations.RemoveField(
            model_name='paymenthistory',
            name='date_creation',
        ),
    ]
