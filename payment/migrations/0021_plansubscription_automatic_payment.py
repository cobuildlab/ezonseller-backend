# Generated by Django 2.0.1 on 2018-04-16 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0020_auto_20180409_1433'),
    ]

    operations = [
        migrations.AddField(
            model_name='plansubscription',
            name='automatic_payment',
            field=models.BooleanField(default=False, help_text='Accept the automatic payment?', verbose_name='Automatic'),
        ),
    ]
