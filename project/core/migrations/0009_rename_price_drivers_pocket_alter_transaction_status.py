# Generated by Django 5.1.4 on 2025-02-13 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_remove_drivers_pocket_drivers_price_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='drivers',
            old_name='price',
            new_name='pocket',
        ),
        migrations.AlterField(
            model_name='transaction',
            name='status',
            field=models.CharField(choices=[('E', 'E'), ('C', 'C'), ('F', 'F'), ('A', 'A'), ('D', 'D'), ('B', 'B')], max_length=50),
        ),
    ]
