# Generated by Django 4.2.4 on 2025-07-01 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orphans', '0021_alter_sponsorship_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sponsorship',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=230, max_digits=10, verbose_name='قيمة الكفالة'),
        ),
    ]
