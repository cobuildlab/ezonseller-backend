# Generated by Django 2.0 on 2018-01-07 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_user_recovery'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='type_plan',
            field=models.CharField(choices=[('free', 'Free'), ('vip', 'Vip')], default='free', max_length=20, verbose_name='Type_plan'),
        ),
    ]
