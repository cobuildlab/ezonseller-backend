# Generated by Django 2.0 on 2018-01-10 13:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_auto_20180110_1256'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='type_plan',
        ),
    ]
