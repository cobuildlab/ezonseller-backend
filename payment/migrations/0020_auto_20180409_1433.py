# Generated by Django 2.0.1 on 2018-04-09 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0019_creditcard_card_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plansubscription',
            name='duration',
            field=models.CharField(blank=True, choices=[('1 month', '1 month'), ('1 year', '1 year')], default='1 month', max_length=50, null=True, verbose_name='Duration'),
        ),
    ]