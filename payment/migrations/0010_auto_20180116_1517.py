# Generated by Django 2.0 on 2018-01-16 15:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('payment', '0009_auto_20180116_0317'),
    ]

    operations = [
        migrations.CreateModel(
            name='CancelSubscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_plan', models.IntegerField(verbose_name='Plan_id')),
                ('reason', models.CharField(max_length=255, verbose_name='Description')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cancel_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='paymenthistory',
            name='automatic_payment',
            field=models.BooleanField(default=False, help_text='Accept the automatic payment?', verbose_name='Automatic'),
        ),
        migrations.AlterField(
            model_name='paymenthistory',
            name='accept',
            field=models.BooleanField(default=False, help_text='Accept the plan?', verbose_name='Accept'),
        ),
    ]