# Generated by Django 2.2 on 2020-07-01 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0005_auto_20200701_0644'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicle',
            name='year',
            field=models.CharField(default='', max_length=4, null=True),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='year_miles',
            field=models.CharField(choices=[('5000', '5,000'), ('12000', '12,000'), ('15000', '15,000'), ('25000', '25,000+')], default='', max_length=20, null=True),
        ),
    ]