# Generated by Django 2.0.1 on 2018-02-02 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0016_auto_20180131_1822'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='creditcard',
            options={'ordering': ['id']},
        ),
        migrations.RemoveField(
            model_name='creditcard',
            name='name',
        ),
        migrations.AddField(
            model_name='creditcard',
            name='first_name',
            field=models.CharField(blank=True, max_length=50, verbose_name='Name'),
        ),
        migrations.AddField(
            model_name='creditcard',
            name='last_name',
            field=models.CharField(blank=True, max_length=50, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='paymenthistory',
            name='cost',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Plan_Cost'),
        ),
        migrations.AlterField(
            model_name='plansubscription',
            name='cost',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Plan_Cost'),
        ),
    ]
