# Generated by Django 2.0.1 on 2018-03-01 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0105_auto_20180128_1942'),
    ]

    operations = [
        migrations.AlterField(
            model_name='amazonassociates',
            name='limit',
            field=models.IntegerField(default=20),
        ),
    ]