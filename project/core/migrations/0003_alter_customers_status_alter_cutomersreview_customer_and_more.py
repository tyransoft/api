# Generated by Django 5.1.4 on 2025-02-08 13:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_rename_decription_transaction_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customers',
            name='status',
            field=models.CharField(choices=[('onride', 'onride'), ('available', 'available')], max_length=30),
        ),
        migrations.AlterField(
            model_name='cutomersreview',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer_ratings', to='core.customers'),
        ),
        migrations.AlterField(
            model_name='drivers',
            name='status',
            field=models.CharField(choices=[('driveing', 'driveing'), ('available', 'available')], max_length=30),
        ),
        migrations.AlterField(
            model_name='driversreview',
            name='driver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='driver_rating', to='core.drivers'),
        ),
        migrations.AlterField(
            model_name='driversreview',
            name='review',
            field=models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='status',
            field=models.CharField(choices=[('F', 'F'), ('B', 'B'), ('E', 'E'), ('D', 'D'), ('A', 'A'), ('C', 'C')], max_length=50),
        ),
    ]
