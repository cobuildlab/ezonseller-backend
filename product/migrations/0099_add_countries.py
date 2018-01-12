from django.db import migrations, models

def create_countires(apps, schema_editor):
    Country = apps.get_model("product", "Country")
    Country.objects.bulk_create([
        Country(name='Brazil', code='BR'),
        Country(name='Canada', code='CA'),
        Country(name='China', code='CN'),
        Country(name='France', code='FR'),	
        Country(name='Germany', code='DE'),	
        Country(name='India', code='IN'),
        Country(name='Italy', code='IT'),	
        Country(name='Japan', code='JP'),
        Country(name='Mexico', code='MX'),	
        Country(name='Spain', code='ES'),
        Country(name='United Kingdom', code='UK'),	
        Country(name='United States', code='US'),
    ])


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_auto_20180111_2321'),
    ]

    operations = [
        migrations.RunPython(create_countires),
    ]