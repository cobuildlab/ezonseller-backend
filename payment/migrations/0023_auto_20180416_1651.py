# Generated by Django 2.0.1 on 2018-04-16 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0022_auto_20180416_1647'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plansubscription',
            name='unlimited_search',
            field=models.BooleanField(default=False, help_text='Accept unlimited searches?', verbose_name='Unlimited Search'),
        ),
    ]
