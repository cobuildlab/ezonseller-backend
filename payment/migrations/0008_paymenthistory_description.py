# Generated by Django 2.0 on 2018-01-16 02:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0007_paymenthistory_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymenthistory',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Description'),
        ),
    ]