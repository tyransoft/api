# Generated by Django 5.1.4 on 2025-02-08 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_customers_status_alter_cutomersreview_customer_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='drivers',
            old_name='licnse_id',
            new_name='license_id',
        ),
        migrations.AlterField(
            model_name='customers',
            name='status',
            field=models.CharField(choices=[('available', 'available'), ('onride', 'onride')], max_length=30),
        ),
        migrations.AlterField(
            model_name='drivers',
            name='status',
            field=models.CharField(choices=[('available', 'available'), ('driveing', 'driveing')], max_length=30),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='status',
            field=models.CharField(choices=[('A', 'A'), ('B', 'B'), ('E', 'E'), ('F', 'F'), ('C', 'C'), ('D', 'D')], max_length=50),
        ),
    ]
