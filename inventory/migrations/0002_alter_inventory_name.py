# Generated by Django 4.2.6 on 2023-10-25 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventory',
            name='name',
            field=models.CharField(blank=True, default='Suffolk Coins Inventory Item', max_length=100, null=True),
        ),
    ]
