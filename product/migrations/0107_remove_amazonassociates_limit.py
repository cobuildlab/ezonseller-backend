# Generated by Django 2.0.1 on 2018-04-16 16:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0106_auto_20180301_1742'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='amazonassociates',
            name='limit',
        ),
    ]
