# Generated by Django 2.1.1 on 2019-10-15 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_product_service'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='service',
            name='created_at',
        ),
        migrations.AlterField(
            model_name='product',
            name='type',
            field=models.CharField(choices=[(5, 'CLOTHES'), (7, 'MEAL'), (6, 'TOYS'), (4, 'ALL')], default=4, max_length=255),
        ),
        migrations.AlterField(
            model_name='service',
            name='service_type',
            field=models.CharField(choices=[(9, 'CLEANING'), (10, 'CARSHARING'), (11, 'CARTERING'), (8, 'ALL')], default=8, max_length=255),
        ),
    ]