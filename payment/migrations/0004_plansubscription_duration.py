# Generated by Django 2.0 on 2018-01-15 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0003_auto_20180111_0413'),
    ]

    operations = [
        migrations.AddField(
            model_name='plansubscription',
            name='duration',
            field=models.CharField(blank=True, choices=[('1 mounth', '1 mounth'), ('3 mounth', '3 mounth'), ('6 mounth', '6 mounth'), ('1 year', '1 year'), ('2 year', '2 year'), ('3 year', '3 year')], max_length=50, null=True, verbose_name='Duration'),
        ),
    ]