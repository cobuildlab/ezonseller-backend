# Generated by Django 2.0 on 2018-01-17 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0099_add_countries'),
    ]

    operations = [
        migrations.AddField(
            model_name='amazonassociates',
            name='limit',
            field=models.IntegerField(default=10),
        ),
    ]
